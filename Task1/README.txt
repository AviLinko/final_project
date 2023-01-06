/************** Description ***************/
In this task we had to perform a simulation on two objects (sensors), 
which are initialized with a direction vector and a position vector.
Depending on the change of the position and direction of the first object, 
the program will return the updated position and direction of the second object.


/*************** Code ******************/
3 files:

Sensor2RM: The program receives the data initialization of both sensors, and receives 2 new random data of sensor 1.
The program calls the function found in the file getRotationMatrix, the function finds the rotation matrix between the angle of sensor 1 in position 0, and the angle of sensor 1 in position 1.
The program will print the updated status of sensor 2.

Sensor2Qu: the same idea as in Sensor2RM, but in Quaternions instead of rotation matrices.

getRotationMatrix: Holds the function that return the rotation matrix of sensor 1.

