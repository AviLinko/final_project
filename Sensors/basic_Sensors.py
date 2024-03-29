import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyquaternion import Quaternion

left_sensor = r"/home/adi/workspace/student_projects/jce_2023/final_project/Sensors/left_sensor.csv"
right_sensor = r"/home/adi/workspace/student_projects/jce_2023/final_project/Sensors/right_sensor.csv"


sensor1_data = pd.read_csv(left_sensor)
sensor2_data = pd.read_csv(right_sensor)

sensor1_pos = sensor1_data[['pose.position.x', 'pose.position.y', 'pose.position.z']].values
sensor1_quat = sensor1_data[['pose.orientation.x', 'pose.orientation.y', 'pose.orientation.z', 'pose.orientation.w']].values

sensor2_pos = sensor2_data[['pose.position.x', 'pose.position.y', 'pose.position.z']].values
sensor2_quat = sensor2_data[['pose.orientation.w','pose.orientation.x', 'pose.orientation.y', 'pose.orientation.z']].values

calibration_matrix = np.array([[-1.0, 0.0, 0.0, 0.0],
                               [0.0, 1.0, 0.0, 0.0],
                               [0.0, 0.0, -1.0, 0.6124],
                               [0.0, 0.0, 0.0, 1.0]])
rotation_matrix = calibration_matrix[:3,:3]
translation_vector = calibration_matrix[:3,3]

sensor2_rot = sensor2_quat[:, :3]

# sensor1_quat_calculated = np.dot(sensor2_rot, calibration_matrix[:3, :3].T)


# sensor1_pos_calculated = np.dot(calibration_matrix, np.concatenate((sensor2_pos.T, np.ones((1, sensor2_pos.shape[0]))))).T
r = []
for q in sensor2_quat:
    q_quat = Quaternion(q)
    r.append(q_quat.rotate(translation_vector))
sensor1_pos_calculated  = sensor1_pos_calculated = np.dot(rotation_matrix,(sensor2_pos+np.array(r)).T).T#+translation_vector
print("Sensor 1 Position: ", sensor1_pos[:3])
start_index = 1000
end_index = 3000
translation_0  = sensor1_pos[start_index,:]-sensor1_pos_calculated[start_index,:]
sensor1_pos_calculated   = sensor1_pos_calculated + translation_0

plt.figure()
for ax in range(3):
    plt.subplot(3,1,ax+1)
    plt.plot(sensor1_pos[start_index:end_index,ax],'.-')
    # plt.plot(sensor2_pos[start_index:end_index,ax],'.-')
    plt.plot(sensor1_pos_calculated[start_index:end_index,ax],'+')
plt.show()

print("Sensor 1 Quaternion: ", sensor1_quat)
