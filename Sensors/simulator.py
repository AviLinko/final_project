import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyquaternion import Quaternion

sensor2 = r"C:\Users\avka9\Desktop\study\projects\final_project\Sensors\s2.csv"

sensor2_data = pd.read_csv(sensor2)

sensor2_pos = sensor2_data[['pose.position.x', 'pose.position.y', 'pose.position.z']].values
sensor2_quat = sensor2_data[['pose.orientation.x', 'pose.orientation.y', 'pose.orientation.z', 'pose.orientation.w']].values

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
sensor1_pos = np.dot(rotation_matrix,(sensor2_pos+np.array(r)).T).T

start_index = 1000
end_index = 4000
translation_0 = sensor1_pos[start_index,:]-sensor1_pos[start_index,:]
sensor1_pos = sensor1_pos + translation_0

plt.figure()
for ax in range(3):
    plt.subplot(3,1,ax+1)
    # plt.plot(sensor1_pos[start_index:end_index,ax],'.-')
    plt.plot(sensor2_pos[start_index:end_index,ax],'.-')
    plt.plot(sensor1_pos[start_index:end_index,ax],'+')
plt.show()

translation_0 = sensor1_pos[0, :] - sensor1_pos[0, :]
sensor1_pos = sensor1_pos - translation_0

sensor1_data = pd.DataFrame(sensor1_pos, columns=["pose.position.x", "pose.position.y", "pose.position.z"])

sensor1_data.to_csv("s1.csv", index=False)