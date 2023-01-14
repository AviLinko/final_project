from scipy.spatial.transform import Rotation as R
import numpy as np

rotation_quat = R.from_euler('z', 90, degrees=True)

# define the quaternion that you want to rotate
original_quat = R.from_quat([0, 0, np.sin(np.pi/4), np.cos(np.pi/4)])

# Multiply the rotation quaternion with the original quaternion
rotated_quat = rotation_quat * original_quat

if __name__ == "__main__":
    print(rotated_quat.as_quat())