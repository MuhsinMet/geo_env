# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 00:02:20 2025

@author: popul
"""
#Importing the neccessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import xarray as xr

# Open the netCDF file
dset = xr.open_dataset(r'C:\Users\popul\Downloads\SRTMGL1_NC.003_Data\N21E039.SRTMGL1_NC.nc')

# Add a breakpoint to inspect variables
#pdb.set_trace()

# Loading elevation data
DEM = np.array(dset.variables['SRTMGL1_DEM'])

# Close the netCDF file
dset.close()

# Adding another breakpoint to inspect DEM dimensions
#pdb.set_trace()

DEM.shape

# Visualize the elevation data
plt.imshow(DEM)
cbar = plt.colorbar()
cbar.set_label('Elevation (m asl)')
plt.show()

# Save the figure
plt.savefig('assignment_1.png', dpi=300)