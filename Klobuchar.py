import matplotlib.pyplot as plt
from mayavi import mlab
import numpy as np

"""
Reference:
https://uk.mathworks.com/matlabcentral/fileexchange/59530-klobuchar-ionospheric-delay-model
"""

# Make sphere
theta, phi = np.mgrid[0:np.pi:101j, 0:2*np.pi:101j]
x, y, z = np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)

# Klobuchar parameters
Alpha = [2.6768E-08,  4.4914E-09, -3.2658E-07, -5.2153E-07]
Beta = [1.3058E+05, -1.1203E+05, -7.0416E+05, -6.4865E+06]

# Geomagnetic latitude
lat = (theta - np.pi/2)/np.pi

# klobuchar model
A = Alpha[0] + Alpha[1] * lat + Alpha[2] * lat**2 + Alpha[3] * lat**3
P = Beta[0] + Beta[1] * lat + Beta[2] * lat**2 + Beta[3] * lat**3

P[P<72000] = 72000 # Where did this threshold come from?
A[A<0] = 0

phi_t = phi/(2*np.pi) * 60*60*24 - 50400 # azimuth measured in time (s)
phase = 2*np.pi*phi_t/P
phase[np.abs(phase) > np.pi/2] = np.pi/2

s = np.abs(A * np.cos(phase))  # colors
s = s / np.max(s)

plt.imshow(s) # how to deal with the discontinuity?
plt.show()

# Display
mlab.figure(1, bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(600, 500))
mlab.mesh(x, y, z, scalars=s, colormap='Spectral')
mlab.view()
mlab.show()
