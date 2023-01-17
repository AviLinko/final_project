from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
import numpy as np

#square
point1 = [1, 1, 2]
point2 = [1, -1, 2]
point3 = [-1, -1, 2]
point4 = [-1, 1, 2]
square = [point1, point2, point3, point4] 

euler_angles1 = np.array([0, 0, 0])
euler_angles2 = np.array([0, 0, np.pi/2])
euler_angles3 = np.array([0, 0, np.pi/4])

r1 = R.from_euler('xyz', euler_angles1)
r2 = R.from_euler('xyz', euler_angles2)
r3 = R.from_euler('xyz', euler_angles3)

diff = r2 * r1.inv()
r3_rotated = diff * r3

print (diff.as_euler('xyz'))
print(r3_rotated.as_euler('xyz'))

rotated_square = [r3_rotated.apply(point) for point in square]
# rotated_square = [r1.apply(point) for point in square]

x = [point[0] for point in rotated_square]
y = [point[1] for point in rotated_square]
z = [point[2] for point in rotated_square] 

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x, y, z, c=['red', 'green', 'blue', 'yellow'])

ax.plot(x, y, z, '-', c='black')

for i in range(4):
    ax.plot([x[i], 0], [y[i], 0], [z[i], 0], '--', c='gray')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()