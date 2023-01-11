import math
from typing import List


def sensor_1():
    size: float = 1.0,
    location: List[float] = [0.0, 0.0, 0.0],
    rotation: List[float] = [0.0, 0.0, 0.0]

def sensor_2():
    size: float = 1.0,
    location: List[float] = [0.0, 0.0, 0.0],
    rotation: List[float] = [0.0, 0.0, 0.0]


 if __name__ == "__main__":
    sensor_1(location=[0.0, 0.0, 0.0])
    sensor_2(location=[0.0, 0.0, 0.0])

    # set keyframe rotation
    sensor_1.rotation_euler = [math.radians(90), 0, 0]
    sensor_2.rotation_euler = [0, 0, math.radians(45)]
    


