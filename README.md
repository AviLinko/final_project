# final_project

Sensor Data simulation

Introduction:
This document provides an analysis of the given Python code, which is designed to align and visualize sensor data and simulate postions between multiple sensors.
The code imports data from multiple sensors, applies calibration matrices to align the data, and then plots the aligned data for comparison. The correctness of the formulas and the logic behind the code will be discussed in detail.

Code Overview: The code consists of several functions that perform the following tasks:
extract_position_and_quaternion: Extracts position and quaternion data from the sensor data.
apply_calibration: Applies the calibration matrix to align the sensor data.
plot_aligned_sensor_data: Plots the aligned sensor data for comparison.
add_sensor: Adds a new sensor and its calibration matrix to the list of sensors and calibration matrices.
display_data_between_sensors: Displays the aligned data between all pairs of sensors.

Formulas and Logic: 
2.1. extract_position_and_quaternion: This function takes a DataFrame (csv) containing sensor data and extracts the position and quaternion values. The position values are stored in array, while the quaternion values are stored in another array.
2.2. apply_calibration:
This function takes the position and quaternion data of two sensors and a calibration matrix. It calculates the aligned position data for the first sensor using the calibration matrix. The rotation matrix and translation vector are extracted from the calibration matrix. The translation vector is rotated using the quaternion data of the second sensor, and the result is added to the position data of the second sensor. The aligned position data is then calculated by multiplying the rotation matrix with the modified position data of the second sensor.
2.3. plot_aligned_sensor_data:
This function takes the position data of the first sensor and the calculated aligned position data. It plots the data for comparison, with each axis (x, y, z) plotted in a separate subplot.
Code Execution: The example code at the end of the script demonstrates how to use the functions to align and visualize sensor data. It reads data from three sensors, adds them to the list of sensors, and applies the calibration matrices. Finally, it calls the display_data_between_sensors function to plot the aligned data between all pairs of sensors.

Conclusion:
The given Python code provides a robust solution for aligning and visualizing sensor data using calibration matrices. The formulas and logic used in the code are correct and effectively align the sensor data for comparison. By following the example code provided, users can easily apply this solution to their own sensor data and visualize the results.
