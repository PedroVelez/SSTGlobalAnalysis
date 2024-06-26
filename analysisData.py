# Global mean Sea Surface Temperatures
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pandas as pd
from matplotlib.dates import DateFormatter
import os

from dask.distributed import Client
from dask import delayed
import dask

# Settings 
year1=1982
year2=2024

# Settings compute de climatoloy
yearC1='1982'
yearC2='1992'



Titulos = ['Oceano Global','Hemisferio norte','Hemisferio sur','AtlanticoNorte', 'Demarcación marina levantino-balear', 'Demarcación marina noratlántica','Demarcación marina canaria','Demarcación sudatlántica','Demarcación Estrecho y Alborán']
Titulos_short = ['GO','NH','SH','NAtl','LEBA', 'NOR','CAN','SUD','ESAL']


# Load data
if os.uname().nodename.lower().find('eemmmbp') != -1:
    base_file = '/Users/pvb/Dropbox/Oceanografia/Data/Satelite/noaa.oisst.v2.highres/NC/sst.day.mean'
    dataDir='./data'
elif os.uname().nodename.lower().find('sagams') != -1:
    base_file = '/Users/pvb/Dropbox/Oceanografia/Data/Satelite/noaa.oisst.v2.highres/NC/sst.day.mean'
    dataDir='./data'
elif os.uname().nodename.lower().find('rossby') != -1:
    base_file = '/data/pvb/Satelite/noaa.oisst.v2.highres/NC/sst.day.mean'
    dataDir = '/home/pvb/Analisis/SSTGlobalAnalysis/data'



print('>>>>> Cargando ficheros de '+base_file)

files = [f'{base_file}.{year}.nc' for year in range(year1, year2+1)]
DS = xr.open_mfdataset(files)

for i in range(0,len(Titulos)):
    titulo = Titulos[i]
    titulo_short = Titulos_short[i]
    
    if titulo_short == 'NH':
        sst = DS.sst.sel(lat=slice(0,65))
        print('>>>>> '+titulo)
    elif titulo_short == 'SH':
        sst = DS.sst.sel(lat=slice( -65, 0))
        print('>>>>> '+titulo)
    elif titulo_short == 'GO':
        sst = DS.sst.sel(lat=slice( -65, 65))
        print('>>>>> '+titulo)
    elif titulo_short == 'NAtl':
        sst = DS.sst.sel(lat=slice(0, 65))
        basins = xr.open_dataset(dataDir+'/basins.nc')
        basin_surf = basins.basin[0]
        basin_surf_interp = basin_surf.interp_like(sst, method='nearest')
        sst = sst.where((basin_surf_interp==1) | (basin_surf_interp==4) ,drop=True)
        print('>>>>> '+titulo)
    elif titulo_short == 'LEBA':
        sst = DS.sst.sel(lat=slice(35.5,42.5)).sel(lon=slice(0,8))
        print('>>>>> '+titulo)        
    elif  titulo_short == 'NOR':
        sst = DS.sst.sel(lat=slice(41.8,46.2)).sel(lon=slice(348.5,359.5))
        print('>>>>> '+titulo)        
    elif  titulo_short == 'CAN':
        sst = DS.sst.sel(lat=slice(24.3,32.5)).sel(lon=slice(338,350))
        print('>>>>> '+titulo)
    elif  titulo_short == 'SUD':
        sst = DS.sst.sel(lat=slice(35.5,37.4)).sel(lon=slice(352,354))
        print('>>>>> '+titulo)
    elif  titulo_short == 'ESAL':
        sst = DS.sst.sel(lat=slice(35.5,37)).sel(lon=slice(354,359))
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
    sst_clim = sst.sel(time=slice(yearC1,yearC2)).groupby('time.dayofyear').mean(dim='time').load();

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

    if titulo_short=='GO' or titulo_short=='NAtl' or titulo_short=='LEBA' or titulo_short=='CAN' or titulo_short=='NOR' or titulo_short=='SUD' or titulo_short=='ESAL':
        sst_anom_LD=sst_anom[-1,:,:]
        sst_anom_LD.to_netcdf(dataDir+'/sstLD_anom_'+titulo_short+'.nc',mode='w')
    
# Monthly analisis
    print('>>>>> Monthly'+titulo+titulo_short)
    sst = sst.resample(time='ME').mean(dim='time',skipna=True).load()

## Calculate global mean weigthtened
    print('    > Compute weigthtened mean')
    weights = np.cos(np.deg2rad(sst.lat))
    weights = weights/weights.max()
    weights.name = "weights"
    sst_weighted = sst.weighted(weights)
    sst_wmean = sst_weighted.mean(("lon", "lat"),skipna=True).load()
    
## Create monthly climatology
    print('    > create climatology')
    sst_clim = sst.sel(time=slice(yearC1,yearC2)).groupby('time.month').mean(dim='time').load();
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

