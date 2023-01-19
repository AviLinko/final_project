from scipy.spatial.transform import Rotation as R
import numpy as np
from getQuaternion import quaternion_from_vectors
import xlsxwriter
"""
    Returns the quaternion that rotates vector `vec1` to vector `vec2`.
"""
workbook = xlsxwriter.Workbook ('QuaTask.xlsx')
sheet = workbook.add_worksheet("quaternion")

def legal_angle(euler_angle):
    for i in range(len(euler_angle)):
        if euler_angle[i] < 0:
            euler_angle[i] += 360
        if euler_angle[i] > 360:
            euler_angle[i] -= 360
    
    return euler_angle

class Sensor:
    def __init__(self, name, rotation, location):
        self.name = name
        self.location = location
        self.rotation = rotation

    def __str__(self):
        return f"{self.name}:\nposition:\n{self.location}\norientation:\n{self.rotation}"


class BothSensors:
    def __init__(self, sensor1, sensor2):
        self.sensor1 = sensor1
        self.sensor2 = sensor2

    def __str__(self):
        return f"{self.sensor1.__str__()}\n{self.sensor2.__str__()}"


    def update_objects(self, r1_displacement, t1_displacement):
        #sensor 1
        r1 = r1_displacement
        t1 = self.sensor1.location
        # sensor 2
        r2 = self.sensor2.rotation
        t2 = self.sensor2.location

        # self.sensor2.location = t2 + np.subtract(t1_displacement , t1)

        # find the difference between r1(t0) and r1(t1)
        q_diff = r1_displacement * r1.inv()
        # angle = 2 * np.arccos(q_diff.as_quat()[-1])
        # axis = q_diff.as_rotvec() / np.sin(angle / 2)
        # print("axis: " + axis)
        # quat = R.from_rotvec(axis)

        r2 *= q_diff.inv().as_quat() 

        # Convert the new rotation of sensor 2 to quaternion representation
        new_r2_quat = r2.as_quat()
        self.sensor2.rotation = new_r2_quat

        self.sensor1.position = t1_displacement
        self.sensor1.orientation = r1_displacement




if __name__ == "__main__":
    sheet.write(0, 0, "new sensor2:")
    for i in range(1, 8):
        r_displacement = R.from_quat([0, 0, np.sin(np.pi*(135/180)), np.cos(np.pi*(135/180))])
        t_displacement = np.array([1,2,1])
        
        orientation_1 = R.from_quat([0, 0, np.sin(np.pi/4), np.cos(np.pi/4)])
        position_1 = np.array([3,3,3])
        sensor1 = Sensor("Sensor 1", position_1, orientation_1)

        position_2 = np.array([3,3,3])
        orientation_2 = R.from_quat([0, 0, np.sin(np.pi/4), np.cos(np.pi/4)])
        sensor2 = Sensor("Sensor 2", position_2, orientation_2)

        sensors = BothSensors(sensor1, sensor2)
        rotation_quat = R.from_rotvec([0, 0, np.pi/2])
        orientation_1 *=  rotation_quat
        print(orientation_1)
        # sensors.update_objects(r_displacement, t_displacement)

        # q1 = R.from_quat([0, 0, np.sin(np.pi/4), np.cos(np.pi/4)])
        # q2 = R.from_quat([0, 0, np.sin(np.pi/4), np.cos(np.pi/4)])


        # str_sensor2 = sensors.sensor2.__str__()
        # print(str_sensor2)
        # sheet.write(i, 0, str_sensor2)
    workbook.close()