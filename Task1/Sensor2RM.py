from getRotationMatrix import rotation_matrix_from_vectors
import numpy as np
import pyautogui
import xlsxwriter

workbook = xlsxwriter.Workbook('Task1.xlsx')
worksheet = workbook.add_worksheet()

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
        rotation_matrix = rotation_matrix_from_vectors(self.sensor1.orientation,o_displacement_1)
        self.sensor2.orientation = np.dot(rotation_matrix, self.sensor2.orientation)
        self.sensor1.position = p_displacement_1
        self.sensor1.orientation = o_displacement_1
       

if __name__ == "__main__":
    
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
    worksheet.write('A1', sensors.sensor2)
    print("new", sensors.sensor2)
    workbook.close()
     
