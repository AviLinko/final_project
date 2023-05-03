import os
import pandas as pd
import numpy as np
from pyquaternion import Quaternion
import matplotlib.pyplot as plt

sensor_folder = r"C:\Users\avka9\Desktop\study\projects\final_project\Sensors\data"
matrix_folder = r"C:\Users\avka9\Desktop\study\projects\final_project\Sensors\rot"

def read_calibration_matrix(file_path): 
    calibration_matrix = pd.read_csv(file_path, header=None).values
    calibration_matrix = pd.to_numpy()
    calibration_matrix = calibration_matrix[:4, :4]
    return calibration_matrix

def extract_rotation_translation(calibration_matrix):
    rotation_matrix = calibration_matrix[:3, :3]
    translation_vector = calibration_matrix[:3, 3]
    return rotation_matrix, translation_vector

def rotation_matrix_to_quaternion(rotation_matrix):
    quaternion = Quaternion(matrix=rotation_matrix)
    return quaternion

sensor_data_list = []
for file in os.listdir(sensor_folder):
    if file.endswith('.csv'):
        sensor_data = pd.read_csv(os.path.join(sensor_folder, file))
        sensor_pos = sensor_data[['pose.position.x', 'pose.position.y', 'pose.position.z']].values
        sensor_quat = sensor_data[['pose.orientation.x', 'pose.orientation.y', 'pose.orientation.z', 'pose.orientation.w']].values
        sensor_data_list.append((sensor_pos, sensor_quat))

matrix_list = []
for file in os.listdir(matrix_folder):
    if file.endswith('.csv'):
        matrix_data = pd.read_csv(os.path.join(matrix_folder, file), header=None)
        matrix_array = matrix_data.values
        matrix_list.append(matrix_array)


for i in range(len(sensor_data_list)-1):
    sensor_pos_s1, sensor_quat_s1 = sensor_data_list[i]
    sensor_pos_s2, sensor_quat_s2 = sensor_data_list[i+1]
    rotation_matrix, translation_vector = extract_rotation_translation(matrix_list[i])
    
    # quaternion_s1 = rotation_matrix_to_quaternion(rotation_matrix)
    s2_rot = sensor_quat_s2[:, :3]
    
    r = []
    for q in sensor_quat_s2:
        q_quat = Quaternion(q)
        r.append(q_quat.rotate(translation_vector))
    sensor1_pos_calculated  = np.dot(rotation_matrix,(sensor_pos_s2+np.array(r)).T).T#+translation_vector
    print("Sensor 1 Position: ", sensor_pos_s1[:3])
    start_index = 1000
    end_index = 3000
    translation_0  = sensor_pos_s1[start_index,:]-sensor1_pos_calculated[start_index,:]
    sensor1_pos_calculated += translation_0

    plt.figure()
    for ax in range(3):
        plt.subplot(3,1,ax+1)
        plt.plot(sensor_pos_s1[start_index:end_index,ax],'.-')
        # plt.plot(sensor2_pos[start_index:end_index,ax],'.-')
        plt.plot(sensor1_pos_calculated[start_index:end_index,ax],'+')
    plt.show()

    print("Sensor 1 Quaternion: ", sensor_quat_s1)






