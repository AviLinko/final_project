from scipy.spatial.transform import Rotation as R
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Sensor:
    def __init__(self, name, translation, rotation):
        self.name = name
        self.translation = translation
        self.rotation = rotation
        point1 = [translation[0]+1,translation[1]+1, translation[2]]
        point2 = [translation[0]+1,translation[1]-1, translation[2]]
        point3 = [translation[0]-1,translation[1]-1, translation[2]]
        point4 = [translation[0]-1,translation[1]+1, translation[2]]
        self.square = [rotation.apply(point) for point in list([point1,point2,point3,point4])]
        
    def __str__(self):
        return f"{self.name}:\nposition:\n{self.translation}\norientation:\n{self.rotation}\nobject:{self.square}"
        

class BothSensors:
    def __init__(self, sensor1, sensor2):
        self.sensor1 = sensor1
        self.sensor2 = sensor2

    def __str__(self):
        return f"{self.sensor1.__str__()}\n{self.sensor2.__str__()}"

    def move(self, s1_new_translation):
        self.sensor2.translation = self.sensor2.translation + (s1_new_translation - self.sensor1.translation)
        ########### todo 
        self.sensor1.translation = s1_new_translation

    def rotate(self, s1_new_rotation):
        r1_t0 = self.sensor1.rotation
        r1_t1 = R.from_quat(s1_new_rotation)
        r2_t1 = self.sensor2.rotation

        diff = euler_angle_difference(r1_t0,r1_t1) 
        r2_t1 *= diff
        self.sensor2.rotation = r2_t1
        self.sensor1.rotation = r1_t1
        # self.sensor1.square = [r1_t1.apply(point) for point in self.sensor1.square]
        # self.sensor2.square = [r2_t1.apply(point) for point in self.sensor2.square]

        
       
def euler_angle_difference(s1_rotation, s1_new_rotation):
    r1 = s1_rotation
    r2 = s1_new_rotation
    
    diff_rot = r2 * r1.inv()
    return diff_rot        
     

if __name__ == "__main__":
    r1 = [1, 0, 0, 0]
    r2 = [1, 0, 0, 0]
    s1_rotation_0 = R.from_quat(r1)
    s2_rotation_0 = R.from_quat(r2)
    
    s1_translation_0 = np.array([0,0,0])
    s2_translation_0 = np.array([0,0,2])

    sensor1 = Sensor("Sensor 1", s1_translation_0, s1_rotation_0)
    sensor2 = Sensor("Sensor 2", s2_translation_0, s2_rotation_0)
    sensors = BothSensors(sensor1, sensor2)

    
    euler_angles = [0, 0, 0, np.pi]
    new_translation_s1 = np.array([0,0,1])

    sensors.move(new_translation_s1)
    sensors.rotate(euler_angles)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    rotated_square = [sensor2.rotation.apply(point) for point in sensor2.square]
    
    x = [point[0] for point in rotated_square]
    y = [point[1] for point in rotated_square]
    z = [point[2] for point in rotated_square] 

    ax.scatter(x, y, z, c=['red', 'green', 'blue', 'yellow'])

    ax.plot(x, y, z, '-', c='black')

    for i in range(4):
        ax.plot([x[i], 0], [y[i], 0], [z[i], 0], '--', c='gray')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    
    plt.show()
   

    
