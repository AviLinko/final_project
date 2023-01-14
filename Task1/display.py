from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

# Define the vector (x, y, z)
x = 1
y = 1
z = 0

# Create a new figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Draw the vector using the quiver() function
ax.quiver(0, 0, 0, x, y, z, color='r')

# Show the plot
plt.show()