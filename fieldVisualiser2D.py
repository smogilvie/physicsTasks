import numpy as np
import matplotlib.pyplot as plt

# initialize the parameters
a = 1000
num_points = 25

x = np.linspace(-10, 10, num_points)
y = np.linspace(-10, 10, num_points)
X, Y = np.meshgrid(x, y)

fx = -0.5 * a * (Y - X)
fy = 0.5 * a * (Y + X)
plt.figure(figsize=(8, 8))
plt.quiver(X, Y, fx, fy, color='blue', alpha=0.5)
# plt.streamplot(X, Y, fx, fy, density=2, color='blue', linewidth=1, arrowsize=1)
plt.text(10, 11, f'a = {a}', fontsize=12)
plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.xlabel("x")
plt.ylabel("y")
plt.axis("equal")
plt.show()
