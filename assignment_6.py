import xarray
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file_name = "/mnt/datawaha/hyex/puthiyma/courses/erse_316/Course_Data/ERA5_Data/download.nc"
dset = xarray.open_dataset(file_name)

# Part 2 : Plotting the time series of air temperature and precipitation
t2m = np.array(dset.variables["t2m"])
tp = np.array(dset.variables["tp"])
latitudes = np.array(dset.variables["latitude"])
longitudes = np.array(dset.variables["longitude"])
time_dt = np.array(dset.variables["time"])

#converting air temperature from Kelvin to Celsius and precipitation from m to mm
t2m = t2m - 273.15
tp = tp * 1000

if t2m.ndim == 4:
    t2m = np.nanmean(t2m, axis=1)
    tp = np.nanmean(tp, axis=1)

#plotting the time series of air temperature and precipitation
df_era5 = pd.DataFrame(index=time_dt)
df_era5['t2m'] = t2m[:, 3, 2]
df_era5['tp'] = tp[:, 3, 2]

df_era5.plot()
plt.savefig("era5_plot.png")

annual_precip = df_era5['tp'].resample('YE').mean()*24*365.25
mean_annual_precip = np.nanmean(annual_precip)
print(f"Mean annual precipitation is {mean_annual_precip} mm")

##############################################
# Part 3 : Calculation of Potential evaporation
##############################################

tmin = df_era5['t2m'].resample('D').min().values
tmax = df_era5['t2m'].resample('D').max().values
tmean = df_era5['t2m'].resample('D').mean().values
lat = 21.25
doy = df_era5['t2m'].resample('D').mean().index.dayofyear

import tools


pe = tools.hargreaves_samani_1982(tmin, tmax, tmean, lat, doy)

ts_index = df_era5['t2m'].resample('D').mean().index
plt.figure()
plt.plot(ts_index, pe, label= 'Potential Evaporation')
plt.xlable = ('Time')
plt.ylabel = ('Potential Evaporation (mm/day)')
plt.savefig('pe_plot.png')

#computing mean annual potential evaporation
mean_annual_pe = np.nanmean(pe)
print(f"Mean annual potential evaporation is {mean_annual_pe} mm/day = {mean_annual_pe*365.25} mm/year")

#computin total volume of water evaporation from the reservoir
reservoir_area = 1.6 #km^2
total_volume = mean_annual_pe*365.25*reservoir_area
print(f"Total volume of water evaporation from the reservoir = {total_volume} m^3")