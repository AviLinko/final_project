import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyquaternion import Quaternion

def calculate_sensor1_data(sensor2_data, calibration_matrix):
    sensor2_pos = sensor2_data[['pose.position.x', 'pose.position.y', 'pose.position.z']].values
    sensor2_quat = sensor2_data[['pose.orientation.w', 'pose.orientation.x', 'pose.orientation.y', 'pose.orientation.z']].values

    rotation_matrix = calibration_matrix[:3, :3]
    translation_vector = calibration_matrix[:3, 3]

    r = []
    for q in sensor2_quat:
        q_quat = Quaternion(q)
        r.append(q_quat.rotate(translation_vector))
    sensor1_pos_calculated = np.dot(rotation_matrix, (sensor2_pos + np.array(r)).T).T

    return sensor1_pos_calculated

def plot_sensor_data(sensor1_data, sensor1_pos_calculated):
    start_index = 1000
    end_index = 4000
    plt.figure()
    for ax in range(3):
        plt.subplot(3, 1, ax + 1)
        plt.plot(sensor1_data[start_index:end_index, ax], '.-')
        plt.plot(sensor1_pos_calculated[start_index:end_index, ax], '+')
    plt.show()

def main():
    right_sensor = r"C:\Users\avka9\Desktop\study\projects\final_project\Sensors\s2.csv"
    sensor2_data = pd.read_csv(right_sensor)

    calibration_matrix = np.array([[-1.0, 0.0, 0.0, 0.0],
                                   [0.0, 1.0, 0.0, 0.0],
                                   [0.0, 0.0, -1.0, 0.6124],
                                   [0.0, 0.0, 0.0, 1.0]])

    sensor1_pos_calculated = calculate_sensor1_data(sensor2_data, calibration_matrix)

    sensor1_data = pd.DataFrame(sensor1_pos_calculated, columns=['pose.position.x', 'pose.position.y', 'pose.position.z'])
    sensor1_data.to_csv('sensor1_calculated.csv', index=False)

    plot_sensor_data(sensor2_data[['pose.position.x', 'pose.position.y', 'pose.position.z']].values, sensor1_pos_calculated)

if __name__ == "__main__":
    main()
