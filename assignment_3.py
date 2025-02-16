#importing libraries
import numpy as np
import pandas as pd
import tools
import matplotlib.pyplot as plt
import xarray as xr

#Part 1: Analyzing ISD data for Jeddah
df_isd = tools.read_isd_csv(r'/mnt/datawaha/hyex/puthiyma/courses/erse_316/Course_Data/41024099999.csv')

#plotting the data
plot = df_isd.plot(title="ISD data for Jeddah")
plt.savefig('/mnt/datawaha/hyex/puthiyma/courses/erse_316/output/isd_plot.png')

############################################
#Part 2: Calculating the heat index for Jeddah
############################################

#Calculating the maximum heat index
df_isd['RH'] = tools.dewpoint_to_rh(df_isd['DEW'].values,df_isd['TMP'].values)
df_isd['HI'] = tools.gen_heat_index(df_isd['TMP'].values,df_isd['RH'].values)

HI_max = df_isd.max()
time_HI_max = df_isd.idxmax()

print(f"The maximum heat index is {HI_max}")
print(f"The date and time of maximum HI is {time_HI_max}")

#Extracting air temperature and relative humidity at time of highest HI
t_and_rh = df_isd.loc[["2024-08-10 11:00:00"]]

print(f"air temperature and relative humidity at time of highest HI is {t_and_rh}")

#Plotting the heat index time series
plt.figure()
df_isd['HI'].plot(title="Heat Index time series of Jeddah")
plt.xlabel("Date")
plt.ylabel("Heat Index (°C)")
plt.savefig('/mnt/datawaha/hyex/puthiyma/courses/erse_316/output/isd_HI_plot.png', dpi=300)

#Resampling to daily data

# Convert hourly data to daily mean HI
df_daily = df_isd.resample('D').mean()
plt.plot(df_daily.index, df_daily['HI'], label="Daily Avg HI (2024)", color='red')
plt.xlabel("Date")
plt.ylabel("Heat Index (°C)")
plt.title("Daily Average Heat Index (HI) in 2024")
plt.legend()
plt.savefig("/mnt/datawaha/hyex/puthiyma/courses/erse_316/output/daily_HI.png", dpi=300)


############################################
#Part 3: Estimating projected increase in air temperature for Jeddah under SSP2-4.5
############################################
file_hist = "/mnt/datawaha/hyex/puthiyma/courses/erse_316/Course_Data/Climate_Model_Data/tas_Amon_GFDL-ESM4_historical_r1i1p1f1_gr1_185001-194912.nc"
file_ssp245 = "/mnt/datawaha/hyex/puthiyma/courses/erse_316/Course_Data/Climate_Model_Data/tas_Amon_GFDL-ESM4_ssp245_r1i1p1f1_gr1_201501-210012.nc"

dset_hist = xr.open_dataset(file_hist)
dset_ssp245 = xr.open_dataset(file_ssp245)

# Computin mean temperature for 1850–1900 (historical) & 2071–2100 (future) globally
mean_1850_1900 = np.mean(dset_hist['tas'].sel(time=slice('1850-01-01', '1900-12-31')), axis=0)
mean_2071_2100_ssp245 = np.mean(dset_ssp245['tas'].sel(time=slice('2071-01-01', '2100-12-31')), axis=0)

# Extracting temperature change in Jedah
jeddah_temp_1850_1900 = mean_1850_1900.sel(lat=21.52, lon=39.16, method='nearest')
jeddah_temp_2071_2100 = mean_2071_2100_ssp245.sel(lat=21.52, lon=39.16, method='nearest')

# Computing projected warming for Jeddah under SSP2-4.5
temp_increase_ssp245 = jeddah_temp_2071_2100 - jeddah_temp_1850_1900
warming_value = temp_increase_ssp245.values
print(f"Projected temperature increase for Jeddah under SSP2-4.5: {warming_value}°C")

#Part 3 : 2
#Applying projected increase in air temperature to the heat index

# Applying the warming scenario to the observed 2024 temperature data
df_isd['TMP_future'] = df_isd['TMP'] + warming_value

# Recalculating the Heat Index with the future temperature data
df_isd['HI_future'] = tools.gen_heat_index(df_isd['TMP_future'].values, df_isd['RH'].values)

#Calculating new HI_max
HI_max_future = df_isd['HI_future'].max()

print(f"Projected highest HI in future climate: {HI_max_future}°C")

# Plot current vs. future Heat Index time series
plt.figure(figsize=(12, 6))
plt.plot(df_isd.index, df_isd['HI'], label='Current HI (2024)', color='blue')
plt.plot(df_isd.index, df_isd['HI_future'], label='Future HI (2071–2100, SSP2-4.5)', color='red')
plt.xlabel("Date")
plt.ylabel("Heat Index (°C)")
plt.title("Projected Impact of Climate Change on Heat Index in Jeddah")
plt.legend()
plt.grid()
plt.savefig("/mnt/datawaha/hyex/puthiyma/courses/erse_316/output/heat_index_climate_change.png", dpi=300)
