import os
import pandas as pd
import numpy as np

sensor_folder = 'path/to/sensor/folder'
matrix_folder = 'path/to/matrix/folder'


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