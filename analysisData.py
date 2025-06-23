# Global mean Sea Surface Temperatures
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pandas as pd

import os

import time

from matplotlib.dates import DateFormatter

import pyproj
from shapely.geometry import Polygon, Point
from shapely.ops import transform

import multiprocessing
from dask.distributed import Client, LocalCluster
import dask

from FuncionesArea import *

from globales import *

# ------------------------------------------------------------------------
# Inicio
# ------------------------------------------------------------------------
    
# Funciones --------------------------------------------------------------
def funcionPrincipal():

    base_file = GlobalSU['DatPath'] + '/Satelite/noaa.oisst.v2.highres/NC/sst.day.mean'
    dataDir   = GlobalSU['AnaPath'] + '/SSTGlobalAnalysis/data'

    # Settings 
    year1=1982
    year2=2025

    # Settings compute de climatoloy
    yearC1='1982'
    yearC2='1991'

    Titulos = ['Oceano Global','Hemisferio norte','Hemisferio sur','AtlanticoNorte']
    Titulos_short = ['GO','NH','SH','NAtl']

    # load data
    print('>>>>> Cargando ficheros de '+base_file)

    files = [f'{base_file}.{year}.nc' for year in range(year1, year2+1)]

    DS = xr.open_mfdataset(files,parallel=True, 
                        combine_attrs= "drop",
                        autoclose = True, data_vars='minimal', coords="minimal")


    for i in range(0,len(Titulos)):
        
        titulo = Titulos[i]
        titulo_short = Titulos_short[i]
        start_time = time.time()
        
        if titulo_short == 'NH':
            sst = DS.sst.sel(lat=slice(0,75))
            print('    > '+titulo)
        elif titulo_short == 'SH':
            sst = DS.sst.sel(lat=slice( -75, 0))
            print('    > '+titulo)
        elif titulo_short == 'GO':
            sst = DS.sst.sel(lat=slice( -75, 75))
            print('    > '+titulo)
        elif titulo_short == 'NAtl':
            sst = DS.sst.sel(lat = slice( 0, 65), lon = slice( 262, 360))
            #Quito el med
            lat_point_list = [40, 40, 30, 30, 40]
            lon_point_list = [354.5, 360, 360, 354.5, 354.5]
            polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
            polygon = transform_polygon(polygon_geom)
            mask = np.array([[point_in_polygon(lon,lat,polygon) 
                    for lon in sst.lon.values] 
                    for lat in sst.lat.values])
            sst = sst.where(~mask)

            #Quito el pacifico 
            lat_point_list = [20,  8,  0, 0, 20]
            lon_point_list = [262, 283, 283, 262,262]

            polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
            polygon = transform_polygon(polygon_geom)
            mask = np.array([[point_in_polygon(lon,lat,polygon) 
                    for lon in sst.lon.values] 
                    for lat in sst.lat.values])
            sst = sst.where(~mask)
            print('    > '+titulo)
            
                        
    # Daily analisis
        print('   >> Daily '+titulo+titulo_short)

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
        sst_anom_LD=sst_anom[-1,:,:]
        sst_anom_LD.to_netcdf(dataDir+'/sstLD_anom_'+titulo_short+'.nc',mode='w')
        
    # Monthly analisis
        #print('   >> Monthly '+titulo+titulo_short)
        #sst = sst.resample(time='ME').mean(dim='time',skipna=True).load()

    ## Calculate global mean weigthtened
        #print('    > Compute weigthtened mean')
        #weights = np.cos(np.deg2rad(sst.lat))
        #weights = weights/weights.max()
        #weights.name = "weights"
        #sst_weighted = sst.weighted(weights)
        #sst_wmean = sst_weighted.mean(("lon", "lat"),skipna=True).load()
        
    ## Create monthly climatology
        #print('    > create climatology')
        #sst_clim = sst.sel(time=slice(yearC1,yearC2)).groupby('time.month').mean(dim='time').load();
    ## Create anomaly
        print('    > Compute anomaly mean')
        #sst_anom = sst.groupby('time.month') - sst_clim
        #sst_anom.load();

    ##Calculate global mean weigthtened
        #print('    > Compute weigthtened mean')
        #weights = np.cos(np.deg2rad(sst.lat))
        #weights = weights/weights.max()
        #weights.name = "weights"
        #sst_anom_weighted = sst_anom.weighted(weights)
        #sst_anom_wmean = sst_anom_weighted.mean(("lon", "lat"),skipna=True).load()
        #sst_anom_wmean_rolling = sst_anom_wmean.rolling(time=12,center=True).mean()
        
    ##Save in netcdf
        print('    > to netcdf')
        #sst_anom.to_netcdf(dataDir+'/sstm_anom_'+titulo_short+'.nc',mode='w')
        #sst_wmean.to_netcdf(dataDir+'/sstm_mean_'+titulo_short+'.nc',mode='w')
        #sst_anom_wmean.to_netcdf(dataDir+'/sstm_anom_mean_'+titulo_short+'.nc',mode='w')

        print("    > %s seconds ---" % (time.time() - start_time))
#---------------------------------------------------------------------<<<<

if __name__ == '__main__':
    cluster = LocalCluster(n_workers=26, threads_per_worker=1)
    client = Client(cluster)
    
    print('>>>>> analysisData ' )
    
    start_time = time.time()
    
    funcionPrincipal()
    
    cluster.close()
    client.close()

    print('      analysisData %6.0f s<<<<<' % (time.time() - start_time))