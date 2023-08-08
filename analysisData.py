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

Titulos = ['Oceano Global','Hemisferio norte','Hemisferio sur','AtlanticoNorte']
Titulos_short = ['GO','NH','SH','NAtl']


# Load data
if os.uname().nodename.lower().find('eemmmbp') != -1:
    base_file = '/Users/pvb/Dropbox/Oceanografia/Data/Satelite/noaa.oisst.v2.highres/NC/sst.day.mean'
elif os.uname().nodename.lower().find('rossby') != -1:
    base_file = '/data/shareddata/Satelite/noaa.oisst.v2.highres/NC/sst.day.mean'
    dataDir = '/home/pvb/Analisis/SSTGlobalAnalysis/data'


print('>>>>> Cargando ficheros de '+base_file)

files = [f'{base_file}.{year}.nc' for year in range(1982, 2024)]
DS = xr.open_mfdataset(files)

for i in range(0,len(Titulos)):
    titulo = Titulos[i]
    titulo_short = Titulos_short[i]
    
    if titulo_short == 'NH':
        sst = DS.sst.sel(lat=slice(0,80))
        print('>>>>> '+titulo)
    elif titulo_short == 'SH':
        sst = DS.sst.sel(lat=slice( -80, 0))
        print('>>>>> '+titulo)
    elif titulo_short == 'GO':
        sst = DS.sst.sel(lat=slice( -80, 80))
        print('>>>>> '+titulo)
    elif titulo_short == 'NAtl':
        sst = DS.sst.sel(lat=slice(0, 80))
        basins = xr.open_dataset('./data/basins.nc')
        basin_surf = basins.basin[0]
        basin_surf_interp = basin_surf.interp_like(sst, method='nearest')
        sst = sst.where((basin_surf_interp==1) | (basin_surf_interp==4) ,drop=True)
        print('>>>>> '+titulo)

                
# Daily analisis
    print('>>>>> Daily'+titulo+titulo_short)

## Calculate global mean weigthtened
    print('    > Compute weigthtened mean')
    weights = np.cos(np.deg2rad(sst.lat))
    weights = weights/weights.max()
    weights.name = "weights"
    sst_weighted = sst.weighted(weights)
    sst_wmean = sst_weighted.mean(("lon", "lat"),skipna=True).load()

## Create monthly climatology
    print('    > create climatology')
    sst_clim = sst.sel(time=slice(year1,year2)).groupby('time.dayofyear').mean(dim='time').load();

## Create anomaly
    sst_anom = sst.groupby('time.dayofyear') - sst_clim

## Calculate global mean anomaly
    print('    > Compute anomaly mean')
    weights = np.cos(np.deg2rad(sst.lat))
    weights = weights/weights.max()
    weights.name = "weights"
    sst_anom_weighted = sst_anom.weighted(weights)
    sst_anom_wmean = sst_anom_weighted.mean(("lon", "lat"),skipna=True).load()

## Save in netcdf
    print('    > Save to netcdf')
    sst_wmean.to_netcdf(dataDir+'/sstd_mean_'+titulo_short+'.nc',mode='w')
    sst_anom_wmean.to_netcdf(dataDir+'/sstd_anom_mean_'+titulo_short+'.nc',mode='w')

    if titulo_short=='GO' or titulo_short=='NAtl':
        sst_anom_LD=sst_anom[-1,:,:]
        sst_anom_LD.to_netcdf(dataDir+'/sstLD_anom_'+titulo_short+'.nc',mode='w')
    
# Monthly analisis
    print('>>>>> Monthly'+titulo+titulo_short)
    sst = sst.resample(time='1M').mean(dim='time',skipna=True).load()

## Calculate global mean weigthtened
    print('    > Compute weigthtened mean')
    weights = np.cos(np.deg2rad(sst.lat))
    weights = weights/weights.max()
    weights.name = "weights"
    sst_weighted = sst.weighted(weights)
    sst_wmean = sst_weighted.mean(("lon", "lat"),skipna=True).load()
    
## Create monthly climatology
    print('    > create climatology')
    sst_clim = sst.sel(time=slice(year1,year2)).groupby('time.month').mean(dim='time').load();
## Create anomaly
    print('    > Compute anomaly mean')
    sst_anom = sst.groupby('time.month') - sst_clim
    sst_anom.load();

##Calculate global mean weigthtened
    print('    > Compute weigthtened mean')
    weights = np.cos(np.deg2rad(sst.lat))
    weights = weights/weights.max()
    weights.name = "weights"
    sst_anom_weighted = sst_anom.weighted(weights)
    sst_anom_wmean = sst_anom_weighted.mean(("lon", "lat"),skipna=True).load()
    sst_anom_wmean_rolling = sst_anom_wmean.rolling(time=12,center=True).mean()
    
##Save in netcdf
    print('    > to netcdf')
    sst_anom.to_netcdf(dataDir+'/sstm_anom_'+titulo_short+'.nc',mode='w')
    sst_wmean.to_netcdf(dataDir+'/sstm_mean_'+titulo_short+'.nc',mode='w')
    sst_anom_wmean.to_netcdf(dataDir+'/sstm_anom_mean_'+titulo_short+'.nc',mode='w')

