# Global mean Sea Surface Temperatures
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pandas as pd
from matplotlib.dates import DateFormatter
import os

# Settings compute de climatoloy
year1='1982'
year2='1992'

Titulos = ['Oceano Global','Hemisferio norte','Hemisferio sur','Norte Canarias']
Titulos_short = ['GO','NH','SH','NCanarias']

# Load data
if os.uname().nodename.lower().find('eemmmbp') != -1:
    base_file = '/Users/pvb/Dropbox/Oceanografia/Data/Satelite/noaa.oisst.v2.highres/NC/sst.day.mean'
elif os.uname().nodename.lower().find('rossby') != -1:
    base_file = '/data/shareddata/Satelite/noaa.oisst.v2.highres/NC/sst.day.mean'

print(base_file)

files = [f'{base_file}.{year}.nc' for year in range(1982, 2024)]
DS = xr.open_mfdataset(files)

for i in range(0,len(Titulos)):
    titulo = Titulos[i]
    titulo_short = Titulos_short[i]
    
    if titulo_short=='NH':
        sst = DS.sst.sel(lat=slice(0,80))
        print(titulo)
    elif titulo_short=='SH':
        sst = DS.sst.sel(lat=slice( -80, 0))
        print(titulo)
    elif titulo_short=='GO':
        sst = DS.sst.sel(lat=slice( -80, 80))
        print(titulo)
    elif titulo_short=='NCanarias':
        sst = DS.sst.sel(lon=360-16.1188,lat=28.5559,method='nearest')
        print(titulo)
                
    
# Monthly analisis
    print('>>>>> Monthly'+titulo+titulo_short)
    sst = sst.resample(time='1M').mean(dim='time',skipna=True).load()

## Calculate global mean weigthtened
    print('    > Mean')
    weights = np.cos(np.deg2rad(sst.lat))
    weights = weights/weights.max()
    weights.name = "weights"
    sst_weighted = sst.weighted(weights)
    sst_wmean = sst_weighted.mean(("lon", "lat"),skipna=True).load()

    ## Create monthly climatology
    sst_clim = sst.sel(time=slice(year1,year2)).groupby('time.month').mean(dim='time').load();
    
#Create anomaly
    print('    > Anomaly mean')
    sst_anom = sst.groupby('time.month') - sst_clim
    sst_anom.load();

# Calculate global mean weigthtened
    weights = np.cos(np.deg2rad(sst.lat))
    weights = weights/weights.max()
    weights.name = "weights"
    sst_anom_weighted = sst_anom.weighted(weights)
    sst_anom_wmean = sst_anom_weighted.mean(("lon", "lat"),skipna=True).load()
    sst_anom_wmean_rolling = sst_anom_wmean.rolling(time=12,center=True).mean()
    
## Save in netcdf
    print('    > to netcdf')
    #sst.to_netcdf('./data/sstm_'+titulo_short+'.nc',mode='w')
    sst_anom.to_netcdf('./data/sstm_anom_'+titulo_short+'.nc',mode='w')
    sst_clim.to_netcdf('./data/sstm_clim_'+titulo_short+'.nc',mode='w')
    sst_wmean.to_netcdf('./data/sstm_mean_'+titulo_short+'.nc',mode='w')
    sst_anom_wmean.to_netcdf('./data/sstm_anom_mean_'+titulo_short+'.nc',mode='w')
    