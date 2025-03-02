import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd


# Opening the downloaded NetCDF file
file_path = "/mnt/datawaha/hyex/puthiyma/courses/erse_316/Course_Data/assignment_5/GRIDSAT-B1.2009.11.25.06.v02r01.nc"
dset = xr.open_dataset(file_path)

# Printing dataset details to understand the available variables
print(dset)

# Extracting the longwave infrared (IR) data
IR = np.array(dset.variables['irwin_cdr']).squeeze()

# Checking the shape of the extracted data
print("Shape of IR Data:", IR.shape)

# Flipping the data vertically to correct its orientation
IR = np.flipud(IR)

# Applying scale and offset to get brightness temperatures in Kelvin
IR = IR * 0.01 + 200

# Converting Kelvin to Celsius for easier interpretation
IR = IR - 273.15

# Plotting the brightness temperature data
plt.figure(figsize=(10, 5))
plt.imshow(IR, extent=[-180.035, 180.035, -70.035, 70.035], aspect='auto')
cbar = plt.colorbar()
cbar.set_label("Brightness Temperature (Degree Celcius)")
plt.title("Brightness Temperature Map (Degree Celcius)")
plt.savefig("brightness_temperature_map.png", dpi=300)

# Marking Jeddah's location on the map for reference
jeddah_lat = 21.5
jeddah_lon = 39.2

plt.figure(figsize=(10, 5))
plt.imshow(IR, extent=[-180.035, 180.035, -70.035, 70.035], aspect='auto')
plt.scatter(jeddah_lon, jeddah_lat, color='red', marker='o', label='Jeddah')
cbar = plt.colorbar()
cbar.set_label("Brightness Temperature (Degree Celcius)")
plt.title("Brightness Temperature Map wih Jeddah (Degree Celcius)")
plt.legend()
plt.savefig("brightness_temperature_map_with_jeddah.png", dpi=300)

# Identifying the time with the lowest brightness temperature over Jeddah
min_temp_time = dset.variables['time'][np.argmin(IR)].values  # Extract NumPy datetime
min_temp_time_str = pd.to_datetime(min_temp_time).strftime('%Y-%m-%d %H:%M:%S UTC')  # Format it as a string

print("Lowest brightness temperature time:", min_temp_time_str)

# ==============================================
# Part 3: Rainfall Estimation (Using All 5 Files)
# ==============================================

# File paths for all 5 GridSat NetCDF files (every 3 hours from 00 to 12 UTC)
file_paths = [
    "/mnt/datawaha/hyex/puthiyma/courses/erse_316/Course_Data/assignment_5/GRIDSAT-B1.2009.11.25.00.v02r01.nc",
    "/mnt/datawaha/hyex/puthiyma/courses/erse_316/Course_Data/assignment_5/GRIDSAT-B1.2009.11.25.03.v02r01.nc",
    "/mnt/datawaha/hyex/puthiyma/courses/erse_316/Course_Data/assignment_5/GRIDSAT-B1.2009.11.25.06.v02r01.nc",
    "/mnt/datawaha/hyex/puthiyma/courses/erse_316/Course_Data/assignment_5/GRIDSAT-B1.2009.11.25.09.v02r01.nc",
    "/mnt/datawaha/hyex/puthiyma/courses/erse_316/Course_Data/assignment_5/GRIDSAT-B1.2009.11.25.12.v02r01.nc"
]

# Constants for the AutoEstimator formula
A = 1.1183e11
b = 3.6382e-2
c = 1.2

# Initializing cumulative rainfall array
cumulative_rainfall = None

# Processing all 5 files to compute cumulative rainfall
for file_path in file_paths:
    dset = xr.open_dataset(file_path)
    IR = np.array(dset.variables['irwin_cdr']).squeeze()
    IR = np.flipud(IR)
    IR_kelvin = IR * 0.01 + 200  # Converting to Kelvin

    # Applying the AutoEstimator formula to compute rainfall rate
    R = A * np.exp(-b * (IR_kelvin ** c))  # Rainfall rate in mm/h

    # Converting from mm/h to mm per 3 hours (since each file represents a 3-hour accumulation)
    R_3h = R * 3  

    # Adding this time period’s rainfall to cumulative total
    if cumulative_rainfall is None:
        cumulative_rainfall = R_3h  # First file initializes the array
    else:
        cumulative_rainfall += R_3h  # Summing up all time periods

# Plotting the cumulative rainfall map
plt.figure(figsize=(10, 5))
plt.imshow(cumulative_rainfall, extent=[-180.035, 180.035, -70.035, 70.035], aspect='auto', cmap='Blues')
cbar = plt.colorbar()
cbar.set_label("Cumulative Rainfall (mm)")
plt.title("Cumulative Rainfall from 00:00 - 12:00 UTC on 25 Nov 2009")
plt.savefig("cumulative_rainfall_map.png", dpi=300)

# ==============================================
# Finding the Time of Maximum Rainfall in Jeddah
# ==============================================

# Getting latitude and longitude variable names dynamically
lat_var = [var for var in dset.variables if 'lat' in var.lower()][0]
lon_var = [var for var in dset.variables if 'lon' in var.lower()][0]

# Identifying Jeddah's position in the dataset
lat_index = np.abs(dset.variables[lat_var].values - jeddah_lat).argmin()
lon_index = np.abs(dset.variables[lon_var].values - jeddah_lon).argmin()

# Creating lists to store rainfall values and corresponding time stamps
rainfall_jeddah = []
time_stamps = []  

# Loop through each file to extract rainfall values and timestamps
for file_path in file_paths:
    dset = xr.open_dataset(file_path)
    IR = np.array(dset.variables['irwin_cdr']).squeeze()
    IR = np.flipud(IR)
    IR_kelvin = IR * 0.01 + 200
    R = A * np.exp(-b * (IR_kelvin ** c))

    # Get rainfall at Jeddah’s coordinates
    rain_value = R[lat_index, lon_index]
    rainfall_jeddah.append(rain_value)

    # listing the corresponding time
    time_value = dset.variables['time'].values
    time_stamps.append(time_value)

    # Print rainfall at each time step
    print(f"Time: {time_value}, Rainfall: {rain_value:.2f} mm")
