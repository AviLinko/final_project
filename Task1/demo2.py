import numpy as np
from scipy.spatial.transform import Rotation

# Define the initial axis system
initial_orientation = Rotation.identity()
initial_position = np.array([0, 0, 0])

# Define the sensor positions relative to the initial axis system
sensor1_position = np.array([1, 0, 0])
sensor2_position = np.array([0, 1, 0])

# Define the rotation transformers for the sensors relative to the initial axis system
sensor1_rotation = Rotation.from_euler('xyz', [0, 0, 45], degrees=True)
sensor2_rotation = Rotation.from_euler('xyz', [0, 0, -45], degrees=True)

# Define the calibration data between the sensors
calibration_matrix = np.array([[1, 0], [0, 1]])

# Define a function to calculate the position of each sensor based on the position of the other sensor
def calculate_positions(sensor1_position, sensor2_position, calibration_matrix):
    # Calculate the relative position of sensor 2 with respect to sensor 1
    relative_position = sensor2_position - sensor1_position
    
    # Map the relative position to the true position using the calibration matrix
    relative_position = np.append(relative_position, [0])
    position = np.dot(calibration_matrix, relative_position.reshape(4, 1))
    
    # Calculate the positions of each sensor relative to the true position
    positions = []
    for i in range(2):
        relative_position_i = np.append(eval(f"sensor{i+1}_position") - position[:3], [1])
        positions.append(np.dot(calibration_matrix, relative_position_i.reshape(4, 1))[:3])
    
    return positions


# Define a function to calculate the orientation of each sensor based on the orientation of the other sensor
def calculate_orientations(sensor1_rotation, sensor2_rotation):
    # Calculate the relative rotation between the sensors
    relative_rotation = sensor2_rotation * sensor1_rotation.inv()
    
    # Convert the relative rotation to a quaternion
    relative_quaternion = relative_rotation.as_quat()
    
    # Calculate the orientation of sensor 2 relative to the initial axis system
    sensor2_orientation = sensor1_rotation * Rotation.from_quat(relative_quaternion)
    
    # Combine the orientations into a single array
    orientations = np.vstack((sensor1_rotation.as_quat(), sensor2_orientation.as_quat()))
    
    return orientations

# Define a function to simulate a reading from a position sensor
def simulate_position_sensor(position, orientation, true_position):
    # Calculate the true position in the local coordinate system of the sensor
    true_position_local = orientation.inv().apply(true_position - position)
    
    # Add some random noise to the true position
    measured_position_local = true_position_local + np.random.normal(0, 0.01, size=3)
    
    # Calculate the measured position in the initial axis system
    measured_position = orientation.apply(measured_position_local) + position
    
    return measured_position

# Define a function to simulate a reading from an orientation sensor
def simulate_orientation_sensor(orientation, true_orientation):
    # Calculate the relative rotation between the true orientation and the sensor orientation
    relative_rotation = orientation.inv() * true_orientation
    
    # Convert the relative rotation to a quaternion
    relative_quaternion = relative_rotation.as_quat()
    
    # Add some random noise to the quaternion
    measured_quaternion = relative_quaternion + np.random.normal(0, 0.01, size=4)
    
    # Calculate the measured orientation relative to the initial axis system
    measured_orientation = orientation * Rotation.from_quat(measured_quaternion)
    
    return measured_orientation

def main():
    # Define the positions and rotations of the sensors relative to the rigid body
    sensor1_position = np.array([0.5, 0, 0])
    sensor2_position = np.array([-0.5, 0, 0])
    sensor1_rotation = Rotation.from_euler('xyz', [0, 0, 0], degrees=True)
    sensor2_rotation = Rotation.from_euler('xyz', [0, 0, 180], degrees=True)
    
    # Define the calibration matrix that maps sensor readings to the true position and orientation
    calibration_matrix = np.array([[1, 0, 0, 0],
                                   [0, 1, 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1]])
    
    # Generate some random data for the true position and orientation of the rigid body
    true_position = np.random.uniform(-1, 1, size=3)
    true_orientation = Rotation.random()
    
    # Calculate the positions and orientations of the sensors based on the initial setup
    positions = calculate_positions(sensor1_position, sensor2_position, calibration_matrix)
    orientations = calculate_orientations(sensor1_rotation, sensor2_rotation)
    
    # Simulate readings from each sensor
    measured_positions = []
    measured_orientations = []
    for i in range(2):
        measured_position = simulate_position_sensor(positions[i], orientations[i], true_position)
        measured_positions.append(measured_position)
        
        measured_orientation = simulate_orientation_sensor(orientations[i], true_orientation)
        measured_orientations.append(measured_orientation)
        
    # Display the results
    print("True position:", true_position)
    print("True orientation:", true_orientation.as_quat())
    print("Measured positions:", measured_positions)
    print("Measured orientations:", [o.as_quat() for o in measured_orientations])
    
if __name__ == '__main__':
    main()
