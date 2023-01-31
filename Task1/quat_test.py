from scipy.spatial.transform import Rotation as R
import numpy as np
import xlsxwriter

workbook = xlsxwriter.Workbook('Task1.xlsx')
sheet = workbook.add_worksheet("Task1")
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
        return f"{self.name}:\nposition:\n{self.translation}\norientation:\n{self.rotation.as_quat()}\n"
        

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

        diff = quat_difference(r1_t0,r1_t1) 
        r2_t1 *= diff
        self.sensor2.rotation = r2_t1
        self.sensor1.rotation = r1_t1
      
 
def quat_difference(s1_rotation, s1_new_rotation):
    r1 = s1_rotation
    r2 = s1_new_rotation
    
    diff_rot = r2 * r1.inv()
    return diff_rot        
     

if __name__ == "__main__":
    sheet.write(0, 0, "new sensor2:")
    for i in range(1, 8):
        q1 = R.from_quat([1, 0, 0, 0])
        q2 = R.from_quat([np.cos(np.pi/4), 0, 0, np.sin(np.pi/4)])
        s1_rotation_0 = q1
        s2_rotation_0 = q2
        
        s1_translation_0 = np.array([0,0,1])
        s2_translation_0 = np.array([0,0,1])

        sensor1 = Sensor("Sensor 1", s1_translation_0, s1_rotation_0)
        sensor2 = Sensor("Sensor 2", s2_translation_0, s2_rotation_0)
        sensors = BothSensors(sensor1, sensor2)

        quaternion = R.random().as_quat()
        new_translation_s1 = np.random.uniform(-5, 5, (3,))

        sensors.move(new_translation_s1)
        sensors.rotate(R.from_quat(quaternion))
        str_sensor2 = sensors.sensor2.__str__()
        str_sensor1 = sensors.sensor1.__str__()
        sheet.write(i, 0, str_sensor2)
        sheet.write(i+8, 0, str_sensor1)
        
    workbook.close()
