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
        self.sensor1.translation = s1_new_translation

    def rotate(self, s1_new_rotation):
        r1_t0 = self.sensor1.rotation
        r1_t1 = s1_new_rotation
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
    q1 = R.from_quat([1, 0, 0, 0])
    q2 = R.from_quat([np.cos(np.pi/4), 0, 0, np.sin(np.pi/4)])
    s1_rotation_0 = q1
    s2_rotation_0 = q2
    
    s1_translation_0 = np.array([0,0,1])
    s2_translation_0 = np.array([0,0,1])

    sensor1 = Sensor("Sensor 1", s1_translation_0, s1_rotation_0)
    sensor2 = Sensor("Sensor 2", s2_translation_0, s2_rotation_0)
    sensors = BothSensors(sensor1, sensor2)
    
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1, projection='3d')
    ax2 = fig.add_subplot(2, 1, 2, projection='3d')
    def update(num):
        ax1.clear()
        ax2.clear()
        euler_angles = R.from_quat([np.cos(num*np.pi/4), 0, 0, np.sin(num*np.pi/4)])
        new_translation_s1 = np.random.rand(3)
        sensors.move(new_translation_s1)
        sensors.rotate(euler_angles)

        # rotated_square1 = [sensor1.rotation.apply(point) for point in sensor1.square]
        # rotated_square2 = [sensor2.rotation.apply(point) for point in sensor2.square]
        rotated_square1 = [np.add(sensor1.rotation.apply(point), sensor1.translation) for point in sensor1.square]
        rotated_square2 = [np.add(sensor2.rotation.apply(point), sensor2.translation) for point in sensor2.square]
        # rotated_square1 = [sensor1.translation.apply(point) for point in sensor2.square]
        # rotated_square2 = [sensor2.translation.apply(point) for point in sensor2.square]

        x1 = [point[0] for point in rotated_square1]
        y1 = [point[1] for point in rotated_square1]
        z1 = [point[2] for point in rotated_square1] 

        x2 = [point[0] for point in rotated_square2]
        y2 = [point[1] for point in rotated_square2]
        z2 = [point[2] for point in rotated_square2] 

        ax1.scatter(x1, y1, z1, c=['red', 'green', 'blue', 'yellow'])
        ax2.scatter(x2, y2, z2, c=['red', 'green', 'blue', 'yellow'])

        ax1.plot(x1, y1, z1, '-', c='black')
        ax2.plot(x2, y2, z2, '-', c='black')
        for i in range(4):
            t1 = sensor1.translation
            t2 = sensor2.translation

            ax1.plot([x1[i], t1[0]], [y1[i],  t1[1]], [z1[i],  t1[2]], '--', c='gray')
            ax2.plot([x2[i], t2[0]], [y2[i],  t2[1]], [z2[i],  t2[2]], '--', c='gray')

        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_zlabel('z')
        
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')
        ax2.set_zlabel('z')

    anim = FuncAnimation(fig, update, frames=range(100), repeat=True, interval = 1000)
    plt.show()
    
