"""
In this experiment we use the hand controller via the sync service to provide target positions and orientations for the end effector of the robot. 

The robot is controlled in the position space, and the inverse kinematics are solved using the ikpy library.

The continous joint type is not supported by the lib https://github.com/Phylliade/ikpy/issues/134

That blocks us for using ikplot for either robot - that sucks.
"""

import ikpy.chain
import numpy as np
import ikpy.utils.plot as plot_utils

my_chain = ikpy.chain.Chain.from_urdf_file("./px100.URDF")

target_position = [ 0.1, -0.2, 0.1]

print("The angles of each joints are : ", my_chain.inverse_kinematics(target_position))

real_frame = my_chain.forward_kinematics(my_chain.inverse_kinematics(target_position))
print("Computed position vector : %s, original position vector : %s" % (real_frame[:3, 3], target_position))

# Optional: support for 3D plotting in the NB
# If there is a matplotlib error, uncomment the next line, and comment the line below it.
# %matplotlib inline

import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')

my_chain.plot(my_chain.inverse_kinematics([2, 2, 2]), ax)
matplotlib.pyplot.show()