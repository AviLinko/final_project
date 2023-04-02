import numpy as np

import pandas as pd

left_sensor = r"C:\Users\avka9\Desktop\study\projects\final_project\Sensors\left_sensor.csv"

right_sensor = r"C:\Users\avka9\Desktop\study\projects\final_project\Sensors\right_sensor.csv"


# read in the sensor data from the csv files

sensor1_data = pd.read_csv(left_sensor)

sensor2_data = pd.read_csv(right_sensor)

# extract position and quaternion data from sensor1

sensor1_pos = sensor1_data[['pose.position.x', 'pose.position.y', 'pose.position.z']].values

sensor1_quat = sensor1_data[['pose.orientation.x', 'pose.orientation.y', 'pose.orientation.z', 'pose.orientation.w']].values

# extract position and quaternion data from sensor2

sensor2_pos = sensor2_data[['pose.position.x', 'pose.position.y', 'pose.position.z']].values

sensor2_quat = sensor2_data[['pose.orientation.x', 'pose.orientation.y', 'pose.orientation.z', 'pose.orientation.w']].values

# define the calibration matrix between sensor1 and sensor2

calibration_matrix = np.array([[0.0, 0.0, 1.0, 0.0],
                               [-1.0, 0.0, 0.0, 0.0],
                               [0.0, -1.0, 0.0, 0.0],
                               [0.0, 0.0, 0.0, 1.0]])

# calculate the transformation matrix to convert sensor2 data to sensor1 data
transformation_matrix = np.dot(np.linalg.inv(calibration_matrix), np.array([[1, 0, 0, -sensor1_pos[0][0]],
                                                                           [0, 1, 0, -sensor1_pos[0][1]],
                                                                           [0, 0, 1, -sensor1_pos[0][2]],
                                                                           [0, 0, 0, 1]]))

# extract the rotation matrix from sensor2_quat and multiply it with the transpose of calibration_matrix
sensor2_rot = sensor2_quat[:, :3]

sensor1_quat = np.dot(sensor2_rot, calibration_matrix[:3, :3].T)


# print out the position and quaternion of sensors

sensor1_pos = np.dot(transformation_matrix, np.concatenate((sensor2_pos.T, np.ones((1, sensor2_pos.shape[0])))))

print("Sensor 1 Position: ", sensor1_pos[:3])

print("Sensor 1 Quaternion: ", sensor1_quat)
