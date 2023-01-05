from getRotationMatrix import rotation_matrix_from_vectors
import numpy as np
import pyautogui

class Sensor:
    def __init__(self, name, position, orientation):
        self.name = name
        self.position = position 
        self.orientation = orientation

    def get_orientation(self):
        return self.orientation

    def get_position(self):
        return self.position

    def __str__(self):
        return f"name:{self.name}\nposition:\n{self.position}\norientation:\n{self.orientation}"


class BothSensors:
    def __init__(self, sensor1, sensor2):
        self.sensor1 = sensor1
        self.sensor2 = sensor2

    def __str__(self):
        return f"{self.sensor1.__str__()}\n{self.sensor2.__str__()}"


def update_objects(position_1, orientation_1, position_2, orientation_2):
    p_displacement_1 = np.random.rand(3)
    o_displacement_1 = np.random.rand(3)

    new_position_2 = position_2 + (p_displacement_1 - position_1)
    rotation_matrix = rotation_matrix_from_vectors(orientation_1,o_displacement_1)

    new_orientation_2 = np.dot(rotation_matrix, orientation_2)
    print("sensor 2 new position:", new_position_2)
    print("sensor 2 new orientation:", new_orientation_2)
    

if __name__ == "__main__":
    
    position_1 = np.random.rand(3)
    orientation_1 = np.random.rand(3)
    sensor1 = Sensor("Sensor 1", position_1, orientation_1)

    position_2 = np.random.rand(3)
    orientation_2 = np.random.rand(3)
    sensor2 = Sensor("Sensor 2", position_2, orientation_2)
    update_objects(position_1, orientation_1, position_2, orientation_2)

     
