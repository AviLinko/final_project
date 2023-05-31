import os
import numpy as np
import pandas as pd
from pyquaternion import Quaternion
import matplotlib.pyplot as plt


def update_plot(time_point, sensor_positions, sensor_directions, ax):
    ax.clear()
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow']
    
    for i, (pos, dirs) in enumerate(zip(sensor_positions, sensor_directions)):
        ax.scatter(*pos, color=colors[i % len(colors)], label=f'Sensor {i + 1}')
        for j, color in enumerate(['r', 'g', 'b']):
            ax.quiver(*pos, *dirs[:, j], color=color, length=0.6, normalize=True)
    
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
        chained_matrix = np.dot(chained_matrix, matrix)
    
    return chained_matrix

def perform_simulation(sensor_folder, calibration_folder):
    sensor_files = [f for f in os.listdir(sensor_folder) if f.startswith('sensor') and f.endswith('.csv')]
    num_sensors = len(sensor_files)
    
    sensor_positions = []
    sensor_orientations = []
    for i in range(1, num_sensors + 1):
        pos, quat = load_sensor_data(sensor_folder, i)
        sensor_positions.append(pos)
        sensor_orientations.append(quat)
    
    calibration_matrices = []
    for i in range(1, num_sensors):
        if i == 1:
            calibration_matrices.append(load_calibration_matrix(calibration_folder, i, i + 1))
        else:
            calibration_matrices.append(chain_calibration_matrices(calibration_folder, 1, i + 1))

    start_index = 1000
    end_index = 3000

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    time_points = range(start_index, end_index)
    for t in time_points:
        sensor_positions_t = [sensor_positions[0][t, :]]
        sensor_directions_t = [np.column_stack([Quaternion(sensor_orientations[0][t, :]).rotate(np.array([1, 0, 0])),
                                                Quaternion(sensor_orientations[0][t, :]).rotate(np.array([0, 1, 0])),
                                                Quaternion(sensor_orientations[0][t, :]).rotate(np.array([0, 0, 1]))])]
        
        for i in range(1, num_sensors):
            rotation_matrix = calibration_matrices[i - 1][:3, :3]
            translation_vector = calibration_matrices[i - 1][:3, 3]
            q2_quat = Quaternion(sensor_orientations[i][t, :])
            r = q2_quat.rotate(translation_vector)
            pos = np.dot(rotation_matrix, (sensor_positions[i][t, :] + r).T).T
            sensor_positions_t.append(pos)
            sensor_directions_t.append(np.column_stack([Quaternion(sensor_orientations[i][t, :]).rotate(np.array([1, 0, 0])),
                                                        Quaternion(sensor_orientations[i][t, :]).rotate(np.array([0, 1, 0])),
                                                        Quaternion(sensor_orientations[i][t, :]).rotate(np.array([0, 0, 1]))]))
        
        update_plot(t, sensor_positions_t, sensor_directions_t, ax)
        if plt.waitforbuttonpress(0.001):
            break

    plt.show()

sensor_folder = 'data'
calibration_folder = 'rot'

perform_simulation(sensor_folder, calibration_folder)
