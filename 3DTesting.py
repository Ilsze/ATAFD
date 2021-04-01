#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 17:08:46 2021

@author: carolineskalla
"""

from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
#%matplotlib notebook
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
"""
#fig = plt.figure()
#ax = plt.axes(projection="3d")

#plt.show()

#example from online

fig = plt.figure()
ax = plt.axes(projection="3d")

z_line = np.linspace(0, 15, 1000)
x_line = np.cos(z_line)
y_line = np.sin(z_line)
#ax.plot3D(x_line, y_line, z_line, 'gray')

z_points = 15 * np.random.random(100)
x_points = np.cos(z_points) + 0.1 * np.random.randn(100)
y_points = np.sin(z_points) + 0.1 * np.random.randn(100)
ax.scatter3D(x_points, y_points, z_points, c=z_points, cmap='hsv');

plt.show()

#another example from online

# Creating dataset
z = np.random.randint(100, size =(50))
x = np.random.randint(80, size =(50))
y = np.random.randint(60, size =(50))
 
# Creating figure
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")
 
# Creating plot
ax.scatter3D(x, y, z, color = "green")
plt.title("simple 3D scatter plot")
 
# show plot
plt.show()


#my example using arrays

fig = plt.figure()
ax = plt.axes(projection="3d")
x = np.array([1,2,3,4,5,6,7,8,9,10])
y = np.array([1,2,3,4,5,6,7,8,9,10])
z = np.array([100, 200, 300, 900, 700, 200, 400, 500, 800, 100])
ax.scatter3D(x, y, z, color = "blue");

#surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm,
  #                     linewidth=0, antialiased=False)
  
fig = plt.figure()
ax = Axes3D(fig)
surf = ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.1)
fig.colorbar(surf, shrink=0.5, aspect=5)
#plt.savefig('teste.pdf')
plt.show()

"""

#surface plot with data points
#import matplotlib.pyplot as plt
#import numpy as np
from scipy.interpolate import griddata

# data coordinates and values
x = np.random.random(100)*10
y = np.random.random(100)*10
z = np.random.random(100)*10


# target grid to interpolate to
#xi = yi = np.arange(0,1.01,0.01)
xi = yi = np.arange(0,10.01,0.1)
xi,yi = np.meshgrid(xi,yi)

# set mask
#mask = (xi > 0.5) & (xi < 0.6) & (yi > 0.5) & (yi < 0.6)

# interpolate
zi = griddata((x,y),z,(xi,yi),method='linear')

# mask out the field
#zi[mask] = np.nan

# plot
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax = Axes3D(fig)

#ax.scatter3D(x, y, z, color = "blue");

#plt.contourf(xi,yi,zi,np.arange(0,1.01,0.01))
fig = plt.figure()
axes = fig.gca(projection ='3d')
axes.plot_surface(xi, yi, zi)
#plt.plot(x,y,'k.')
plt.xlabel('xi',fontsize=16)
plt.ylabel('yi',fontsize=16)
plt.show()
#plt.savefig('interpolated.png',dpi=100)
#plt.close(fig)
"""


#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
  
#a = np.array([1, 2, 3])
#b = np.array([4, 5, 6, 7])
  
#a, b = np.meshgrid(a, b)
  
# surface plot for a**2 + b**2
a = np.arange(-1, 1, 0.02)
b = a
a, b = np.meshgrid(a, b)


  
fig = plt.figure()
axes = fig.gca(projection ='3d')
axes.plot_surface(a, b, a**2 + b**2)
  
plt.show()


"""
"""
from scipy.interpolate import griddata

a = [1,2,3,4,5,6,7,8,9]
b = [1,2,3,4,5,6,7,8,9]
c = [4, 20, 12, 8, 15, 21, 30, 5, 10]

ai, bi = np.meshgrid(a, b)
ci = griddata((a,b),c,(ai,bi),method='linear')
"""