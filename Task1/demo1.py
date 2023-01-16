from scipy.spatial.transform import Rotation as R
import numpy as np
def euler_angle_difference(eu1, eu2):
    # create rotation objects from the initial and new Euler angles
    r1 = R.from_euler('xyz', eu1)
    r2 = R.from_euler('xyz', eu2)
    # find the difference between the two rotations
    diff_rot = r2 * r1.inv()
    # extract the Euler angles of the difference rotation
    diff_euler = diff_rot.as_euler('xyz')
    return diff_euler

eu1 = [0, 0, 0]
eu2 = [0, 0, np.pi / 4]
# eu3 = [0, 0, np.pi / 6]

print(euler_angle_difference(eu1, eu2)) # [0. 0. 0.7854]
# print(euler_angle_difference(eu1, eu3)) # [0. 0. 0.5236]