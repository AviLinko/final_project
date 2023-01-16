from scipy.spatial.transform import Rotation as R
import numpy as np

class Sensor:
    def __init__(self, name, location, rotation):
        self.name = name
        self.location = location
        self.rotation = rotation
        point1 = [location[0]+1,location[1]+1, location[2]]
        point2 = [location[0]+1,location[1]-1, location[2]]
        point3 = [location[0]-1,location[1]-1, location[2]]
        point4 = [location[0]-1,location[1]+1, location[2]]
        self.square = [point1, point2, point3, point4]

    def __str__(self):
        return f"{self.name}:\nposition:\n{self.location}\norientation:\n{self.rotation}\nobject:{self.square}"
        

class BothSensors:
    def __init__(self, sensor1, sensor2):
        self.sensor1 = sensor1
        self.sensor2 = sensor2

    def __str__(self):
        return f"{self.sensor1.__str__()}\n{self.sensor2.__str__()}"

    def move_location(self, position):
        self.sensor2.location = self.sensor2.location + (position - self.sensor1.location)
        self.sensor1.location = position 

    def rotate_and_move(self, s1_new_rotation):
        self.sensor2.rotation *= (euler_angle_difference(self.sensor1.rotaion, s1_new_rotation))
        self.sensor1.square *= s1_new_rotation
        self.sensor2.square *= self.sensor2.rotation
       
def euler_angle_difference(eu0, new_eu):
    r1 = R.from_euler('xyz', eu0)
    r2 = R.from_euler('xyz', new_eu)
    
    diff_rot = r2 * r1.inv()
    diff_euler = diff_rot.as_euler('xyz')
    return diff_euler        
     


if __name__ == "__main__":
   
    s1_r = R.from_euler('xyz', [0, 0, 0], degrees=True)
    s2_r = R.from_euler('xyz', [0, 0, 0], degrees=True)
    
    s1_position_0 = np.array([0,0,0])
    s2_position_0 = np.array([3,3,3])

    sensor1 = Sensor("Sensor 1", s1_position_0, s1_r)
    sensor2 = Sensor("Sensor 2", s2_position_0, s2_r)
    sensors = BothSensors(sensor1, sensor2)
    for i in range(7):
        r1 = R.random()
        new_point_s1 = np.random.rand(3)
        orientation_1 = r1.as_euler("xyz", degrees=True)

        sensors.move_location(new_point_s1)
        diff = euler_angle_difference (sensor1.rotation, orientation_1)
        sensors.rotate_and_move(orientation_1)

        print(sensor1.rotation)
        print(sensor1.location)
        print(sensor2.square)

    

   

    
