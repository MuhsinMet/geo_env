#Importing Required Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import xarray as xr

#opening the historical dataset
file_hist = "/mnt/datawaha/hyex/puthiyma/courses/erse_316/Course_Data/Climate_Model_Data/tas_Amon_GFDL-ESM4_historical_r1i1p1f1_gr1_185001-194912.nc"
dset_hist = xr.open_dataset(file_hist)

#Calculateing the Mean Air Temperature Map for 1850–1900
mean_1850_1900 = np.mean(dset_hist['tas'].sel(time=slice('1850-01-01', '1900-12-31')), axis=0)

# Converting to NumPy Array
mean_1850_1900 = np.array(mean_1850_1900)

#pdb.set_trace()

# printiing the properties of the variable
print("Mean 1850-1900 Data Type:", mean_1850_1900.dtype)
print("Mean 1850-1900 Shape:", mean_1850_1900.shape)

#Loading other files for Future Climate Model Datasets (2071-2100)
file_ssp119 = "/mnt/datawaha/hyex/puthiyma/courses/erse_316/Course_Data/Climate_Model_Data/tas_Amon_GFDL-ESM4_ssp119_r1i1p1f1_gr1_201501-210012.nc"
file_ssp245 = "/mnt/datawaha/hyex/puthiyma/courses/erse_316/Course_Data/Climate_Model_Data/tas_Amon_GFDL-ESM4_ssp245_r1i1p1f1_gr1_201501-210012.nc"
file_ssp585 = "/mnt/datawaha/hyex/puthiyma/courses/erse_316/Course_Data/Climate_Model_Data/tas_Amon_GFDL-ESM4_ssp585_r1i1p1f1_gr1_201501-210012.nc"

# Opening each dataset
dset_ssp119 = xr.open_dataset(file_ssp119)
dset_ssp245 = xr.open_dataset(file_ssp245)
dset_ssp585 = xr.open_dataset(file_ssp585)

# Computing Mean Air Temperature Maps for Each Climate Scenario
mean_2071_2100_ssp119 = np.mean(dset_ssp119['tas'].sel(time=slice('2071-01-01', '2100-12-31')), axis=0)
mean_2071_2100_ssp245 = np.mean(dset_ssp245['tas'].sel(time=slice('2071-01-01', '2100-12-31')), axis=0)
mean_2071_2100_ssp585 = np.mean(dset_ssp585['tas'].sel(time=slice('2071-01-01', '2100-12-31')), axis=0)

# Converting to NumPy arrays
mean_2071_2100_ssp119 = np.array(mean_2071_2100_ssp119)
mean_2071_2100_ssp245 = np.array(mean_2071_2100_ssp245)
mean_2071_2100_ssp585 = np.array(mean_2071_2100_ssp585)

# Computing Temperature Differences
temp_change_ssp119 = mean_2071_2100_ssp119 - mean_1850_1900
temp_change_ssp245 = mean_2071_2100_ssp245 - mean_1850_1900
temp_change_ssp585 = mean_2071_2100_ssp585 - mean_1850_1900

# Visualizing the Temperature Differences
def plot_temp_change(temp_data, scenario, filename):

    plt.figure(figsize=(10, 5))
    plt.imshow(temp_data, cmap='coolwarm', origin='lower')
    plt.colorbar(label="Temperature Change (K)")
    plt.title(f"Projected Temperature Change (2071–2100 vs. 1850–1900) - {scenario}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig(filename, dpi=300)
    plt.show()

# Ploting temperature change maps for each SSP scenario
plot_temp_change(temp_change_ssp119, "SSP119", "temp_change_ssp119.png")
plot_temp_change(temp_change_ssp245, "SSP245", "temp_change_ssp245.png")
plot_temp_change(temp_change_ssp585, "SSP585", "temp_change_ssp585.png")

