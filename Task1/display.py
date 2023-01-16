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

euler_angles = [np.pi/4, 0, 0] 

r = R.from_euler('xyz', euler_angles)

rotated_square = [r.apply(point) for point in square]

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