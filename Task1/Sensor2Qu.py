import numpy as np
from getQuaternion import quaternion_from_vectors
import xlsxwriter
"""
    Returns the quaternion that rotates vector `vec1` to vector `vec2`.
"""
workbook = xlsxwriter.Workbook('QuTask.xlsx')
sheet = workbook.add_worksheet("quaternion")
class Sensor:
    def __init__(self, name,position, orientation):
        self.name = name
        self.position = position
        self.orientation = orientation

    def __str__(self):
        return f"{self.name}:\nposition:\n{self.position}\norientation:\n{self.orientation}"


class BothSensors:
    def __init__(self, sensor1, sensor2):
        self.sensor1 = sensor1
        self.sensor2 = sensor2

    def __str__(self):
        return f"{self.sensor1.__str__()}\n{self.sensor2.__str__()}"

    def update_objects(self, p_displacement_1, o_displacement_1):
        
        self.sensor2.position = self.sensor2.position + (p_displacement_1 - self.sensor1.position)
        quat = quaternion_from_vectors (self.sensor1.orientation,o_displacement_1)
        self.sensor2.orientation = rotate_vector(self.sensor2.orientation, quat)
        self.sensor1.position = p_displacement_1
        self.sensor1.orientation = o_displacement_1
       
"""
    Rotates a 3D vector `vec` using the quaternion `quat`.
"""
def rotate_vector(vec, quat):
    vec_quat = np.concatenate((vec, [0]))
    rotated_quat = quat_mult(quat, quat_mult(vec_quat, quat_conj(quat)))
    
    return rotated_quat[:4]

def quat_mult(q1, q2):
    """
    Multiplies quaternion `q1` by quaternion `q2`.
    """
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1*w2 - x1*x2 - y1*y2 - z1*z2
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 - x1*z2 + y1*w2 + z1*x2
    z = w1*z2 + x1*y2 - y1*x2 + z1*w2
    return np.array([w, x, y, z])

def quat_conj(q):
    """
    Returns the conjugate of quaternion `q`.
    """
    w, x, y, z = q
    return np.array([w, -x, -y, -z])

if __name__ == "__main__":
    sheet.write(0, 0, "new sensor2:")
    for i in range(1, 8):
        p_displacement_1 = np.random.rand(3)
        o_displacement_1 = np.random.rand(3)
        
        position_1 = np.random.rand(3)
        orientation_1 = np.random.rand(3)
        sensor1 = Sensor("Sensor 1", position_1, orientation_1)

        position_2 = np.random.rand(3)
        orientation_2 = np.random.rand(3)
        sensor2 = Sensor("Sensor 2", position_2, orientation_2)

        sensors = BothSensors(sensor1, sensor2)
        sensors.update_objects( p_displacement_1, o_displacement_1)
        str_sensor2 = sensors.sensor2.__str__()
        print(str_sensor2)
        sheet.write(i, 0, str_sensor2)
    workbook.close()