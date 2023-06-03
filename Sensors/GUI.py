import os
import json
import numpy as np
import pandas as pd
from pyquaternion import Quaternion
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, ttk

def update_plot(time_point, sensor_positions, sensor_directions, ax, sensor_fusion_enabled=False):
    ax.clear()
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow']
    
    if sensor_fusion_enabled:
        pos, dirs = sensor_positions[-1], sensor_directions[-1]
        ax.scatter(*pos, color='red', label='Fused Sensor')
        for j, color in enumerate(['r', 'g', 'b']):
            ax.quiver(*pos, *dirs[:, j], color=color, length=0.6, normalize=True)
    else:
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

def sensor_fusion(sensor_positions, sensor_orientations):
    fused_position = np.mean(sensor_positions, axis=0)
    
    num_orientations = len(sensor_orientations)
    q_matrix = np.zeros((4, 4))
    
    for q_float in sensor_orientations:
        q = Quaternion(q_float)
        q_matrix += np.outer(q.elements, q.elements)
    
    q_matrix /= num_orientations
    eigenvalues, eigenvectors = np.linalg.eig(q_matrix)
    max_eigenvalue_index = np.argmax(eigenvalues)
    fused_orientation = Quaternion(eigenvectors[:, max_eigenvalue_index])
    
    return fused_position, fused_orientation



def perform_simulation(sensor_file, calibration_matrices, selected_sensors=None, sensor_fusion_enabled=False):
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

        if sensor_fusion_enabled:
            fused_position, fused_orientation = sensor_fusion(sensor_positions_t, [sensor_orientations[t, :] for _ in range(len(sensor_positions_t))])
            sensor_positions_t.append(fused_position)
            sensor_directions_t.append(np.column_stack([fused_orientation.rotate(np.array([1, 0, 0])),
                                                        fused_orientation.rotate(np.array([0, 1, 0])),
                                                        fused_orientation.rotate(np.array([0, 0, 1]))]))

        update_plot(t, sensor_positions_t, sensor_directions_t, ax, sensor_fusion_enabled)
        if plt.waitforbuttonpress(0.001):
            break

    plt.show()


def run_simulation():
    sensor_file = r"C:\Users\avka9\Desktop\study\projects\final_project\Sensors\left_sensor.csv"
    calibration_file = r"C:\Users\avka9\Desktop\study\projects\final_project\Sensors\matrices.json" 
    calibration_matrices = load_calibration_matrices_from_json(calibration_file)

    if simulation_type_var.get() == "All Sensors":
        perform_simulation(sensor_file, calibration_matrices)
    elif simulation_type_var.get() == "2 Sensors":
        selected_sensors = [int(sensor1_entry.get()), int(sensor2_entry.get())]
        perform_simulation(sensor_file, calibration_matrices, selected_sensors)
    elif simulation_type_var.get() == "Sensor Fusion":
        perform_simulation(sensor_file, calibration_matrices, sensor_fusion_enabled=True)

root = tk.Tk()
root.title("Sensor Simulation")

simulation_type_var = tk.StringVar(value="All Sensors")

simulation_type_label = ttk.Label(root, text="Simulation Type:")
simulation_type_label.grid(column=0, row=0, sticky="W")
simulation_type_combobox = ttk.Combobox(root, textvariable=simulation_type_var, values=["All Sensors", "2 Sensors", "Sensor Fusion"])
simulation_type_combobox.grid(column=1, row=0, sticky="W")


sensor1_label = ttk.Label(root, text="Sensor 1:")
sensor1_label.grid(column=0, row=1, sticky="W")
sensor1_entry = ttk.Entry(root)
sensor1_entry.grid(column=1, row=1, sticky="W")

sensor2_label = ttk.Label(root, text="Sensor 2:")
sensor2_label.grid(column=0, row=2, sticky="W")
sensor2_entry = ttk.Entry(root)
sensor2_entry.grid(column=1, row=2, sticky="W")

run_button = ttk.Button(root, text="Run Simulation", command=run_simulation)
run_button.grid(column=1, row=3, sticky="W")

root.mainloop()