from scipy.spatial.transform import Rotation as R
import numpy as np

class Sensor:
    def __init__(self, name, location, rotation):
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

    def rotate_and_move(self, position, quaternion):
        self.sensor2.location += (position - self.sensor1.location)
        ratio = quaternion.inv() * self.sensor1.rotation
        self.sensor2.rotation = ratio * self.sensor2.rotation
       
        


if __name__ == "__main__":
    s1_position_0 = np.array([1,1,1])
    s1_orientation_0 = R.from_quat([0, 0, np.sin(np.pi/4), np.cos(np.pi/4)])
    sensor1 = Sensor("Sensor 1", s1_position_0, s1_orientation_0)

    s2_position_0 = np.array([3,3,3])
    s2_orientation_0 = R.from_quat([0, 0, np.sin(np.pi/4), np.cos(np.pi/4)])
    sensor2 = Sensor("Sensor 2", s2_position_0, s2_orientation_0)

    sensors = BothSensors(sensor1, sensor2)

    position_1 = np.array([2,2,2])
    orientation_1 = R.from_quat([0, 0, np.sin(np.pi/2), np.cos(np.pi/2)])
    
    sensors.rotate_and_move(position_1, orientation_1)
    print(orientation_1.as_quat())
    print([0, 0, np.sin(np.pi/2), np.cos(np.pi/2)])
    print(s1_orientation_0.as_quat())
    print(sensor2.location, sensor2.rotation.as_quat())

    
