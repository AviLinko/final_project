import openslam_gmapping as gmapping
import numpy as np

slam = gmapping.GridSlamProcessor()

sensor_config = {
    "laser": {
        "min_range": 0.1,
        "max_range": 30.0,
        "max_beams": 180,
        "angular_resolution": np.radians(1.0),
        "pose": np.array([0.0, 0.0, 0.0])
    },
    "imu": {
        "pose": np.array([0.0, 0.0, 0.0])
    },
    "gps": {
        "pose": np.array([0.0, 0.0, 0.0])
    },
    "gyrometer": {
        "pose": np.array([0.0, 0.0, 0.0])
    },
    "accelerometer": {
        "pose": np.array([0.0, 0.0, 0.0])
    }
}

for sensor_type, sensor_params in sensor_config.items():
    if sensor_type == "laser":
        laser_params = gmapping.LaserParams(
            sensor_params["min_range"], 
            sensor_params["max_range"], 
            sensor_params["max_beams"], 
            sensor_params["angular_resolution"]
        )
        slam.addLaserSensor("laser", laser_params)

    elif sensor_type == "imu":
        imu_pose = gmapping.Pose3D(
            sensor_params["pose"][0], 
            sensor_params["pose"][1], 
            sensor_params["pose"][2],
            0.0, 0.0, 0.0, 1.0
        )
        slam.addIMUSensor("imu", imu_pose)

    elif sensor_type == "gps":
        gps_pose = gmapping.Pose3D(
            sensor_params["pose"][0], 
            sensor_params["pose"][1], 
            sensor_params["pose"][2],
            0.0, 0.0, 0.0, 1.0
        )
        slam.addGPSSensor("gps", gps_pose)
    
    elif sensor_type == "gyrometer":
        gyro_pose = gmapping.Pose3D(
            sensor_params["pose"][0], 
            sensor_params["pose"][1], 
            sensor_params["pose"][2],
            0.0, 0.0, 0.0, 1.0
        )
        slam.addGyroSensor("gyrometer", gyro_pose)
    
    elif sensor_type == "accelerometer":
        accel_pose = gmapping.Pose3D(
            sensor_params["pose"][0], 
            sensor_params["pose"][1], 
            sensor_params["pose"][2],
            0.0, 0.0, 0.0, 1.0
        )
        slam.addAccelSensor("accelerometer", accel_pose)

for measurement in measurements:
    if measurement["type"] == "laser":
        # Get laser measurements
        laser_data = measurement["data"]
        
        # Process laser measurements
        scan = gmapping.Observation(laser_data, "laser")
        slam.processScan(scan)

    elif measurement["type"] == "imu":
        # Get IMU measurements
        imu_data = measurement["data"]