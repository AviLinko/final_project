import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyquaternion import Quaternion

def align_sensor_data(sensor1_file, sensor2_file, calibration_matrix):
    sensor1_data = pd.read_csv(sensor1_file)
    sensor2_data = pd.read_csv(sensor2_file)

    sensor1_pos, sensor1_quat = extract_position_and_quaternion(sensor1_data)
    sensor2_pos, sensor2_quat = extract_position_and_quaternion(sensor2_data)

    sensor1_pos_calculated = apply_calibration(sensor1_pos, sensor2_pos, sensor2_quat, calibration_matrix)

    plot_aligned_sensor_data(sensor1_pos, sensor1_pos_calculated)

    return sensor1_pos_calculated

def extract_position_and_quaternion(sensor_data):
    pos = sensor_data[['pose.position.x', 'pose.position.y', 'pose.position.z']].values
    quat = sensor_data[['pose.orientation.w', 'pose.orientation.x', 'pose.orientation.y', 'pose.orientation.z']].values
    return pos, quat

def apply_calibration(sensor1_pos, sensor2_pos, sensor2_quat, calibration_matrix):
    rotation_matrix = calibration_matrix[:3, :3]
    translation_vector = calibration_matrix[:3, 3]

    r = []
    for q in sensor2_quat:
        q_quat = Quaternion(q)
        r.append(q_quat.rotate(translation_vector))
    sensor1_pos_calculated = np.dot(rotation_matrix, (sensor2_pos + np.array(r)).T).T

    start_index = 1000
    translation_0 = sensor1_pos[start_index, :] - sensor1_pos_calculated[start_index, :]
    sensor1_pos_calculated = sensor1_pos_calculated + translation_0

    return sensor1_pos_calculated

def plot_aligned_sensor_data(sensor1_pos, sensor1_pos_calculated):
    start_index = 1000
    end_index = 3000

    plt.figure()
    for ax in range(3):
        plt.subplot(3, 1, ax + 1)
        plt.plot(sensor1_pos[start_index:end_index, ax], '.-')
        plt.plot(sensor1_pos_calculated[start_index:end_index, ax], '+')
    plt.show()

# exmple:

# left_sensor = r"C:\Users\avka9\Desktop\study\projects\final_project\Sensors\left_sensor.csv"
# right_sensor = r"C:\Users\avka9\Desktop\study\projects\final_project\Sensors\right_sensor.csv"
# calibration_matrix = np.array([[-1.0, 0.0, 0.0, 0.0],
#                                [0.0, 1.0, 0.0, 0.0],
#                                [0.0, 0.0, -1.0, 0.6124],
#                                [0.0, 0.0, 0.0, 1.0]])

# aligned_data = align_sensor_data(left_sensor, right_sensor, calibration_matrix)
