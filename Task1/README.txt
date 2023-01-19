/************** Description ***************/

The following code illustrates 2 sensors on a rigid body,
 that each of the sensors depends on the rotation and translation of the other.
When sensor 1 rotates or moves, the program will calculate its rotation and translation ratio,
 and report the new translation and rotation of the second sensor.
To illustrate the issue, the program will display 2 screens illustrating the rotation of sensor 2
 according to the rotation of sensor 1.

/************** Code *************/

Class Sensor
The Sensor class takes in 3 parameters upon initialization:

name: a string representing the name of the sensor
translation: a numpy array representing the translation of the sensor in 3D space
rotation: a rotation object from the scipy.spatial.transform.Rotation module, representing the orientation of the sensor
It also has a class variable square which is a list of points that represents the square shape of the sensor in 3D space.

It has a __str__ method that returns a string representation of the sensor's name, translation, orientation, and square.

Class BothSensors
The BothSensors class takes in 2 parameters upon initialization:

sensor1: an instance of the Sensor class
sensor2: another instance of the Sensor class
It has a __str__ method that returns a string representation of both sensors by calling the __str__ method of each sensor.

It has a move method that takes in a parameter s1_new_translation,
 which is a numpy array representing the new translation of sensor1. 
The method updates the translation of sensor2 by adding the difference between the new translation of sensor1 and its current translation.

It also has a rotate method that takes in a parameter s1_new_rotation, 
which is a list of 3 numbers representing the new Euler angles of sensor1. 
It updates the rotation of both sensors by using the euler_angle_difference() function and the scipy.spatial.transform.Rotation module.

Function euler_angle_difference()
The euler_angle_difference() function takes in 2 parameters:

s1_rotation: a rotation object from the scipy.spatial.transform.Rotation module, representing the current orientation of sensor1
s1_new_rotation: a rotation object from the scipy.spatial.transform.Rotation module, representing the new orientation of sensor1
It returns the difference rotation between the current and new orientations of sensor1 using the scipy.spatial.transform.Rotation module.

****** Example usage
In the if __name__ == "__main__" block, the code creates instances of the Sensor and BothSensors classes, 
and uses them to demonstrate how to move and rotate the sensors in 3D space.
 It also uses the matplotlib library to create a 3D animation of the sensors' movement and rotation.








