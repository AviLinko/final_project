import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pyquaternion import Quaternion
import time

sensor2 = r"/home/adi/workspace/student_projects/jce_2023/final_project/Sensors/s2.csv"
sensor1 = r"/home/adi/workspace/student_projects/jce_2023/final_project/Sensors/s1.csv"

sensor2_data = pd.read_csv(sensor2)

sensor2_pos = sensor2_data[['pose.position.x', 'pose.position.y', 'pose.position.z']].values
sensor2_quat = sensor2_data[['pose.orientation.x', 'pose.orientation.y', 'pose.orientation.z', 'pose.orientation.w']].values


sensor_1_data = pd.read_csv(sensor2)
sensor1_pos = sensor_1_data[['pose.position.x', 'pose.position.y', 'pose.position.z']].values
sensor1_quat = sensor_1_data[['pose.orientation.x', 'pose.orientation.y', 'pose.orientation.z', 'pose.orientation.w']].values
calibration_matrix = np.array([[-1.0, 0.0, 0.0, 0.0],
                               [0.0, 1.0, 0.0, 0.0],
                               [0.0, 0.0, -1.0, 0.6124],
                               [0.0, 0.0, 0.0, 1.0]])
rotation_matrix = calibration_matrix[:3, :3]
translation_vector = calibration_matrix[:3, 3]

r = []
for q in sensor2_quat:
    q_quat = Quaternion(q)
    r.append(q_quat.rotate(translation_vector))
sensor1_pos_calc = np.dot(rotation_matrix, (sensor2_pos + np.array(r)).T).T

start_index = 1000
end_index = 4000
translation_0 = sensor1_pos[start_index, :] - sensor2_pos[start_index, :]
sensor1_pos_calc = sensor1_pos_calc + translation_0

# translation_0 = sensor2_pos[0, :] - sensor1_pos[0, :]
# sensor1_pos = sensor1_pos + translation_0

def update_plot(time_point, sensor1, sensor2, sensor3, ax):
    ax.clear()
    ax.scatter(*sensor1, color='red', label='Sensor 1')
    ax.scatter(*sensor2, color='blue', label='Sensor 2')
    ax.scatter(*sensor3, color='green', label='Sensor 1_calculated')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title(f'Time: {time_point}')
    ax.legend()
    plt.pause(0.02)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

time_points = range(start_index, end_index)
for t in time_points:
    s1 = sensor1_pos[t, :]
    s2 = sensor2_pos[t, :]
    s3 = sensor1_pos_calc[t,:]
    update_plot(t, s1, s2,s3, ax)
    if plt.waitforbuttonpress(0.001):
        break

plt.show()

sensor1_data = pd.DataFrame(sensor1_pos, columns=['pose.position.x', 'pose.position.y', 'pose.position.z'])
sensor1_data.to_csv('sensor1_calculated.csv', index=False)