# final_project
degree final project

This is a  Python script that performs a simulation based on sensor data and calibration parameters. It includes functions for loading sensor data, calibration matrices, and performing the simulation. Here's a summary of what the code does:

-The update_plot function is defined to update the 3D plot with sensor positions, 
calculated positions, and direction vectors at a given time point.
-The load_sensor_data function loads the sensor data from CSV files, extracting position and quaternion values.
-The load_calibration_matrix function loads the calibration matrix from a CSV file based on the given sensor numbers.
-The chain_calibration_matrices function loads multiple calibration matrices and chains them together by matrix multiplication.
-The perform_simulation function performs the simulation. It loads sensor data, determines the appropriate
calibration matrix (either single or chained), calculates the rotation and translation values, and performs quaternion and position calculations.

The simulation results are plotted in a 3D plot using the update_plot function.

The user is prompted to enter the sensor numbers and the simulation is performed by calling the perform_simulation function.

In summary, the code reads sensor data and calibration parameters, performs quaternion and position calculations based on the calibration, and visualizes the results in a 3D plot.
