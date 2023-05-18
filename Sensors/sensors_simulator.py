import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pyquaternion import Quaternion
import os

def update_plot(time_point, sensor1, sensor2, sensor1_calculated, sensor1_dir, sensor2_dir, ax):
    ax.clear()
    ax.scatter(*sensor1, color='red', label='Sensor 1')
    ax.scatter(*sensor2, color='blue', label='Sensor 2')
    ax.scatter(*sensor1_calculated, color='green', label='Sensor 1_calculated')
    ax.quiver(*sensor1, *sensor1_dir, color='red', length=0.6, normalize=True)
    ax.quiver(*sensor2, *sensor2_dir, color='blue', length=0.6, normalize=True)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title(f'Time: {time_point}')
    ax.legend()
    plt.pause(0.001)

def load_sensor_data(sensor_folder, sensor_number):
    sensor_file = os.path.join(sensor_folder, f'sensor{sensor_number}.csv')
    sensor_data = pd.read_csv(sensor_file)
    sensor_pos = sensor_data[['pose.position.x', 'pose.position.y', 'pose.position.z']].values
    sensor_quat = sensor_data[['pose.orientation.x', 'pose.orientation.y', 'pose.orientation.z', 'pose.orientation.w']].values
    return sensor_pos, sensor_quat

def load_calibration_matrix(calibration_folder, sensor1, sensor2):
    calibration_file = os.path.join(calibration_folder, f's{sensor1}_to_s{sensor2}.csv')
    calibration_matrix = pd.read_csv(calibration_file).values
    return calibration_matrix

def chain_calibration_matrices(calibration_folder, sensor1, sensor2):
    matrices = []
    for i in range(sensor1, sensor2):
        matrix = load_calibration_matrix(calibration_folder, i, i + 1)
        matrices.append(matrix)
    
    chained_matrix = matrices[0]
    for matrix in matrices[1:]:
        # check if this calculation give us the chain calculation!
        chained_matrix = np.dot(chained_matrix, matrix)
    
    return chained_matrix

def perform_simulation(sensor1, sensor2, sensor_folder, calibration_folder):
    sensor1_pos, sensor1_quat = load_sensor_data(sensor_folder, sensor1)
    sensor2_pos, sensor2_quat = load_sensor_data(sensor_folder, sensor2)
    
    if sensor2 - sensor1 == 1:
        calibration_matrix = load_calibration_matrix(calibration_folder, sensor1, sensor2)
    else:
        calibration_matrix = chain_calibration_matrices(calibration_folder, sensor1, sensor2)

    calibration_matrix = load_calibration_matrix(calibration_folder, sensor1, sensor2)
    rotation_matrix = calibration_matrix[:3, :3]
    translation_vector = calibration_matrix[:3, 3]

    r = []
    sensor1_quat_calc = []
    for q2, q1 in zip(sensor2_quat, sensor1_quat):
        q2_quat = Quaternion(q2)
        r.append(q2_quat.rotate(translation_vector))
        q1_quat = Quaternion(q1)
        sensor1_quat_calc.append((q2_quat*q1_quat).elements)
    sensor1_quat_calc = np.array(sensor1_quat_calc)

    sensor1_pos_calc = np.dot(rotation_matrix, (sensor2_pos + np.array(r)).T).T

    start_index = 1000
    end_index = 3000

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    time_points = range(start_index, end_index)
    for t in time_points:
        s1 = sensor1_pos[t, :]
        s2 = sensor2_pos[t, :]
        s1_calculated = sensor1_pos_calc[t, :]
        s1_dir = Quaternion(sensor1_quat[t, :]).rotate(np.array([1, 0, 0]))
        s2_dir = Quaternion(sensor2_quat[t, :]).rotate(np.array([1, 0, 0]))
        update_plot(t, s1, s2, s1_calculated, s1_dir, s2_dir, ax)
        if plt.waitforbuttonpress(0.001):
            break

    plt.show()

sensor_folder = 'data'
calibration_folder = 'rot'

sensor1 = int(input("Enter the first sensor number: "))
sensor2 = int(input("Enter the second sensor number: "))

perform_simulation(sensor1, sensor2, sensor_folder, calibration_folder)

