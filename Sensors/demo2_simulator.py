import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pyquaternion import Quaternion
import time

def update_plot(time_point, sensor1, sensor2, sensor3, sensor1_dir, sensor2_dir, ax):
    ax.clear()
    ax.scatter(*sensor1, color='red', label='Sensor 1')
    ax.scatter(*sensor2, color='blue', label='Sensor 2')
    ax.scatter(*sensor3, color='green', label='Sensor 1_calculated')

    for i, color in enumerate(['r', 'g', 'b']):
        ax.quiver(*sensor1, *sensor1_dir[:, i], color=color, length=0.7, normalize=True)

    for i, color in enumerate(['r', 'g', 'b']):
        ax.quiver(*sensor2, *sensor2_dir[:, i], color=color, length=0.7, normalize=True)

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title(f'Time: {time_point}')
    ax.legend()
    plt.pause(0.001)

sensor2 = r"C:\Users\avka9\Desktop\study\projects\final_project\Sensors\right_sensor.csv"
sensor1 = r"C:\Users\avka9\Desktop\study\projects\final_project\Sensors\left_sensor.csv"

sensor2_data = pd.read_csv(sensor2)
sensor2_pos = sensor2_data[['pose.position.x', 'pose.position.y', 'pose.position.z']].values
sensor2_quat = sensor2_data[['pose.orientation.x', 'pose.orientation.y', 'pose.orientation.z', 'pose.orientation.w']].values

sensor1_data = pd.read_csv(sensor1)
sensor1_pos = sensor1_data[['pose.position.x', 'pose.position.y', 'pose.position.z']].values
sensor1_quat = sensor1_data[['pose.orientation.x', 'pose.orientation.y', 'pose.orientation.z', 'pose.orientation.w']].values

calibration_matrix = np.array([[-1.0, 0.0, 0.0, 0.0],
                               [0.0, 1.0, 0.0, 0.0],
                               [0.0, 0.0, -1.0, 0.6124],
                               [0.0, 0.0, 0.0, 1.0]])
rotation_matrix = calibration_matrix[:3, :3]
translation_vector = calibration_matrix[:3, 3]

r = []
sensor1_quat_calc = []
for q2, q1 in zip(sensor2_quat, sensor1_quat):
    q2_quat = Quaternion(q2)
    r.append(q2_quat.rotate(translation_vector))
    q1_quat = Quaternion(q1)
    sensor1_quat_calc.append((q2_quat * q1_quat).elements)
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
    s3 = sensor1_pos_calc[t, :]
    
    s1_quat = Quaternion(sensor1_quat[t, :])
    s1_dir = np.column_stack([s1_quat.rotate(np.array([1, 0, 0])),
                              s1_quat.rotate(np.array([0, 1, 0])),
                              s1_quat.rotate(np.array([0, 0, 1]))])

    s2_quat = Quaternion(sensor2_quat[t, :])
    s2_dir = np.column_stack([s2_quat.rotate(np.array([1, 0, 0])),
                              s2_quat.rotate(np.array([0, 1, 0])),
                              s2_quat.rotate(np.array([0, 0, 1]))])

    update_plot(t, s1, s2, s3, s1_dir, s2_dir, ax)
    if plt.waitforbuttonpress(0.001):
        break

plt.show()

# sensor1_data_calc_pos = pd.DataFrame(sensor1_pos_calc, columns=['pose.position.x', 'pose.position.y', 'pose.position.z'])
# sensor1_data_calc_pos.to_csv('sensor1_calculated_position.csv', index=False)

# sensor1_data_calc_quat = pd.DataFrame(sensor1_quat_calc, columns=['pose.orientation.x', 'pose.orientation.y', 'pose.orientation.z', 'pose.orientation.w'])
# sensor1_data_calc_quat.to_csv('sensor1_calculated_quaternion.csv', index=False)
