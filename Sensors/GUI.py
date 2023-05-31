import os
import json
import numpy as np
import pandas as pd
from pyquaternion import Quaternion
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, ttk

def update_plot(time_point, sensor_positions, sensor_directions, ax):
    ax.clear()
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow']
    
    for i, (pos, dirs) in enumerate(zip(sensor_positions, sensor_directions)):
        ax.scatter(*pos, color=colors[i % len(colors)], label=f'Sensor {i + 1}')
        for j, color in enumerate(['r', 'g', 'b']):
            ax.quiver(*pos, *dirs[:, j], color=color, length=0.6, normalize=True)
    
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title(f'Time: {time_point}')
    ax.legend()
    plt.pause(0.001)

def load_sensor_data(sensor_file):
    sensor_data = pd.read_csv(sensor_file)
    sensor_pos = sensor_data[['pose.position.x', 'pose.position.y', 'pose.position.z']].values
    sensor_quat = sensor_data[['pose.orientation.x', 'pose.orientation.y', 'pose.orientation.z', 'pose.orientation.w']].values
    return sensor_pos, sensor_quat

def load_calibration_matrices_from_json(json_file):
    with open(json_file, 'r') as f:
        calibration_matrices = json.load(f)
    return [np.array(matrix) for matrix in calibration_matrices]

def perform_simulation(sensor_file, calibration_matrices, selected_sensors=None):
    sensor_positions, sensor_orientations = load_sensor_data(sensor_file)

    num_sensors = len(calibration_matrices) + 1

    if selected_sensors:
        start_sensor, end_sensor = selected_sensors
    else:
        start_sensor, end_sensor = 1, num_sensors

    start_index = 1000
    end_index = 3000

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    time_points = range(start_index, end_index)
    for t in time_points:
        sensor_positions_t = [sensor_positions[t, :]]
        sensor_directions_t = [np.column_stack([Quaternion(sensor_orientations[t, :]).rotate(np.array([1, 0, 0])),
                                                Quaternion(sensor_orientations[t, :]).rotate(np.array([0, 1, 0])),
                                                Quaternion(sensor_orientations[t, :]).rotate(np.array([0, 0, 1]))])]

        for i in range(start_sensor, end_sensor):
            rotation_matrix = calibration_matrices[i - 1][:3, :3]
            translation_vector = calibration_matrices[i - 1][:3, 3]
            q2_quat = Quaternion(sensor_orientations[t, :])
            r = q2_quat.rotate(translation_vector)
            pos = np.dot(rotation_matrix, (sensor_positions[t, :] + r).T).T
            sensor_positions_t.append(pos)
            sensor_directions_t.append(np.column_stack([Quaternion(sensor_orientations[t, :]).rotate(np.array([1, 0, 0])),
                                                        Quaternion(sensor_orientations[t, :]).rotate(np.array([0, 1, 0])),
                                                        Quaternion(sensor_orientations[t, :]).rotate(np.array([0, 0, 1]))]))

        update_plot(t, sensor_positions_t, sensor_directions_t, ax)
        if plt.waitforbuttonpress(0.001):
            break

    plt.show()


def browse_sensor_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    sensor_file_var.set(file_path)

def browse_calibration_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    calibration_file_var.set(file_path)

def run_simulation():
    sensor_file = sensor_file_var.get()
    calibration_file = calibration_file_var.get()
    calibration_matrices = load_calibration_matrices_from_json(calibration_file)

    if simulation_type_var.get() == "All Sensors":
        perform_simulation(sensor_file, calibration_matrices)
    elif simulation_type_var.get() == "2 Sensors":
        selected_sensors = [int(sensor1_entry.get()), int(sensor2_entry.get())]
        perform_simulation(sensor_file, calibration_matrices, selected_sensors)

root = tk.Tk()
root.title("Sensor Simulation")

sensor_file_var = tk.StringVar()
calibration_file_var = tk.StringVar()
simulation_type_var = tk.StringVar(value="All Sensors")

sensor_file_label = ttk.Label(root, text="Sensor File:")
sensor_file_label.grid(column=0, row=0, sticky="W")
sensor_file_entry = ttk.Entry(root, textvariable=sensor_file_var)
sensor_file_entry.grid(column=1, row=0, sticky="W")
sensor_file_button = ttk.Button(root, text="Browse", command=browse_sensor_file)
sensor_file_button.grid(column=2, row=0, sticky="W")

calibration_file_label = ttk.Label(root, text="Calibration File:")
calibration_file_label.grid(column=0, row=1, sticky="W")
calibration_file_entry = ttk.Entry(root, textvariable=calibration_file_var)
calibration_file_entry.grid(column=1, row=1, sticky="W")
calibration_file_button = ttk.Button(root, text="Browse", command=browse_calibration_file)
calibration_file_button.grid(column=2, row=1, sticky="W")

simulation_type_label = ttk.Label(root, text="Simulation Type:")
simulation_type_label.grid(column=0, row=2, sticky="W")
simulation_type_combobox = ttk.Combobox(root, textvariable=simulation_type_var, values=["All Sensors", "2 Sensors"])
simulation_type_combobox.grid(column=1, row=2, sticky="W")

sensor1_label = ttk.Label(root, text="Sensor 1:")
sensor1_label.grid(column=0, row=3, sticky="W")
sensor1_entry = ttk.Entry(root)
sensor1_entry.grid(column=1, row=3, sticky="W")

sensor2_label = ttk.Label(root, text="Sensor 2:")
sensor2_label.grid(column=0, row=4, sticky="W")
sensor2_entry = ttk.Entry(root)
sensor2_entry.grid(column=1, row=4, sticky="W")

run_button = ttk.Button(root, text="Run Simulation", command=run_simulation)
run_button.grid(column=1, row=5, sticky="W")

root.mainloop()
