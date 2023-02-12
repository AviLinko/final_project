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

class AllSensors:
    def __init__(self, sensors):
        self.sensors = sensors

    def __str__(self):
        return '\n'.join([sensor.__str__() for sensor in self.sensors])

    def move(self, s1_new_translation, s1_index):
        for i, sensor in enumerate(self.sensors):
            if i == s1_index:
                sensor.translation = s1_new_translation
            else:
                sensor.translation = sensor.translation + (s1_new_translation - self.sensors[s1_index].translation)

    def rotate(self, s1_new_rotation, s1_index):
        for i, sensor in enumerate(self.sensors):
            if i == s1_index:
                sensor.rotation = s1_new_rotation
                continue
            r1_t0 = self.sensors[s1_index].rotation
            r1_t1 = s1_new_rotation
            r2_t1 = sensor.rotation

            diff = quat_difference(r1_t0,r1_t1) 
            r2_t1 *= diff
            sensor.rotation = r2_t1

def quat_difference(s1_rotation, s1_new_rotation):
    r1 = s1_rotation
    r2 = s1_new_rotation
    
    diff_rot = r2 * r1.inv()
    return diff_rot        
     

if __name__ == "__main__":
    sheet.write(0, 0, "new sensors:")
    for i in range(1, 8):
        sensors = []
        for j in range(7):
            q = R.from_quat(np.random.uniform(-1, 1, (4,)))
            s_rotation_0 = q
            s_translation_0 = np.random.uniform(-5, 5, (3,))

            sensor = Sensor(f"Sensor {j+1}", s_translation_0, s_rotation_0)
            sensors.append(sensor)
        
        quaternion = R.random().as_quat()
        new_translation_s1 = np.random.uniform(-5, 5, (3,))

        all_sensors = AllSensors(sensors)
        all_sensors.move(new_translation_s1, 0)
        all_sensors.rotate(R.from_quat(quaternion), 0)
        
        for j, sensor in enumerate(sensors):
            str_sensor = sensor.__str__()
            sheet.write(i, j, str_sensor)

    workbook.close()

