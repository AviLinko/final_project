import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyquaternion import Quaternion


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


def add_sensor(sensor_file, calibration_matrix, sensors_data, calibration_matrices):
    sensor_data = pd.read_csv(sensor_file)
    sensor_pos, sensor_quat = extract_position_and_quaternion(sensor_data)
    sensors_data.append((sensor_pos, sensor_quat))
    calibration_matrices.append(calibration_matrix)


def display_data_between_sensors(sensors_data, calibration_matrices):
    num_sensors = len(sensors_data)
    for i in range(num_sensors):
        for j in range(i + 1, num_sensors):
            sensor1_pos, _ = sensors_data[i]
            sensor2_pos, sensor2_quat = sensors_data[j]
            calibration_matrix = calibration_matrices[j - 1]
            sensor1_pos_calculated = apply_calibration(sensor1_pos, sensor2_pos, sensor2_quat, calibration_matrix)
            print(f"Displaying data between sensor {i + 1} and sensor {j + 1}")
            plot_aligned_sensor_data(sensor1_pos, sensor1_pos_calculated)


# Example :  for Aviaaaaddddd

# sensors_data = []
# calibration_matrices = []

# sensor1_file = r"C:\path\to\sensor1.csv"
# add_sensor(sensor1_file, None, sensors_data, calibration_matrices)

# sensor2_file = r"C:\path\to\sensor2.csv"
# calibration_matrix_1_2 = np.array([[-1.0, 0.0, 0.0, 0.0],
#                                    [0.0, 1.0, 0.0, 0.0],
#                                    [0.0, 0.0, -1.0, 0.6124],
#                                    [0.0, 0.0, 0.0, 1.0]])
# add_sensor(sensor2_file, calibration_matrix_1_2, sensors_data, calibration_matrices)

# sensor3_file = r"C:\path\to\sensor3.csv"
# calibration_matrix_2_3 = np.array([[1.0, 0.0, 0.0, 0.0],
#                                    [0.0, -1.0, 0.0, 0.0],
#                                    [0.0, 0.0, 1.0, 0.6124],
#                                    [0.0, 0.0, 0.0, 1.0]])
# add_sensor(sensor3_file, calibration_matrix_2_3, sensors_data, calibration_matrices)

# display_data_between_sensors(sensors_data, calibration_matrices)
