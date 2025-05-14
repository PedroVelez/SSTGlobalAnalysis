# Global mean Sea Surface Temperatures
import numpy as np
import xarray as xr
import pandas as pd

import os

import time

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
    imagesDir = GlobalSU['AnaPath'] + '/SSTGlobalAnalysis/images'

    # Settings 
    year1=1982
    year2=2025

    # Settings compute de climatoloy
    yearC1='1982'
    yearC2='1992'

    Titulos = ['Iberian Canary Basin','Demarcación marina levantino-balear', 'Demarcación marina noratlántica','Demarcación marina canaria','Demarcación sudatlántica','Demarcación Estrecho y Alborán']
    Titulos_short = ['IBICan','LEB', 'NOR','CAN','SUD','ESA']

    # Load data
    print('>>>>> Cargando ficheros de '+base_file)

    files = [f'{base_file}.{year}.nc' for year in range(year1, year2+1)]
    DS = xr.open_mfdataset(files,parallel=True, 
                        combine_attrs= "drop",
                        autoclose = True, data_vars='minimal', coords="minimal")

    # For each demarcacion
    for i in range(0,len(Titulos)):
        titulo = Titulos[i]
        titulo_short = Titulos_short[i]
        start_time = time.time()
        
        demCoord = []
        longDem, latiDem = [], []
        with open('./data/Demarcacion'+titulo_short+'.txt', 'r') as f:
            for line in f:
            # Split the line by whitespace and append the values
                longitude, latitude = map(float, line.split())
                longitude=longitude+360
                longDem.append(longitude)
                latiDem.append(latitude)
                demCoord.append((longitude,latitude))
        demPolygon = Polygon(demCoord)    
        demPolygon_transformed = transform_polygon(demPolygon)

        # Select the data for the demarcacion
        if titulo_short == 'LEB':
            slicelatitude=slice(36,43)
            slicelongitude=slice(358,368)
            sst=DS.sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
            mask = np.array([[point_in_polygon(lon,lat,demPolygon_transformed) 
            for lon in sst.lon.values] 
            for lat in sst.lat.values])
            sst_unmasked = sst
            sst = sst.where(mask)
            print('>>>>> '+titulo)        

        elif  titulo_short == 'NOR':
            slicelatitude=slice(41.25,47)
            slicelongitude=slice(345,360)
            sst=DS.sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
            mask = np.array([[point_in_polygon(lon,lat,demPolygon_transformed) 
            for lon in sst.lon.values] 
            for lat in sst.lat.values])
            sst_unmasked = sst
            sst = sst.where(mask)
            print('>>>>> '+titulo)        
            
        elif  titulo_short == 'CAN':
            slicelatitude=slice(24,32.5)
            slicelongitude=slice(335,350)
            sst=DS.sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
            mask = np.array([[point_in_polygon(lon,lat,demPolygon_transformed) 
            for lon in sst.lon.values] 
            for lat in sst.lat.values])
            sst_unmasked = sst
            sst = sst.where(mask)
            print('>>>>> '+titulo)    

        elif  titulo_short == 'SUD':
            slicelatitude=slice(35.5,37.5)
            slicelongitude=slice(352,354.5)
            sst=DS.sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
            mask = np.array([[point_in_polygon(lon,lat,demPolygon_transformed) 
            for lon in sst.lon.values] 
            for lat in sst.lat.values])
            sst_unmasked = sst
            sst = sst.where(mask)
            print('>>>>> '+titulo)

        elif  titulo_short == 'ESA':
            slicelatitude=slice(35.5,37)
            slicelongitude=slice(354,358.5)
            sst=DS.sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
            mask = np.array([[point_in_polygon(lon,lat,demPolygon_transformed) 
            for lon in sst.lon.values] 
            for lat in sst.lat.values])
            sst_unmasked = sst
            sst = sst.where(mask)
            print('>>>>> '+titulo)
        elif  titulo_short == 'IBICan':
            #sst = DS.sst.sel(lat=slice(20, 50),lon=slice(325,360))
            #basins = xr.open_dataset(dataDir+'/basins.nc')
            #basin_surf = basins.basin[0]
            #basin_surf_interp = basin_surf.interp_like(sst, method='nearest')
            #sst = sst.where((basin_surf_interp==1) ,drop=True)
            sst = DS.sst.sel(lat=slice(20, 47),lon=slice(325,360))
            # Para blanquear el mediterraneo
            lat_point_list = [40, 40, 30, 30, 40]
            lon_point_list = [354.5, 360, 360, 354.5, 354.5]
            polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
            polygon = transform_polygon(polygon_geom)
            mask = np.array([[point_in_polygon(lon,lat,polygon) 
                    for lon in sst.lon.values] 
                    for lat in sst.lat.values])
            
            sst = sst.where(~mask)
            print('>>>>> '+titulo)
                                
    # Daily analisis
        print('>>>>> Daily ')

    ## Calculate global mean weigthtened
        print('    > Compute weigthtened mean')
        weights = np.cos(np.deg2rad(sst.lat))
        weights = weights/weights.max()
        weights.name = "weights"
        sst_weighted = sst.weighted(weights)
        sst_wmean = sst_weighted.mean(("lon", "lat"),skipna=True)

    ## Create monthly climatology
        print('    > create climatology')
        sst_clim = sst.sel(time=slice(yearC1,yearC2)).groupby('time.dayofyear').mean(dim='time')

    ## Create anomaly
        sst_anom = sst.groupby('time.dayofyear') - sst_clim

    ## Calculate global mean anomaly
        print('    > Compute anomaly mean')
        weights = np.cos(np.deg2rad(sst.lat))
        weights = weights/weights.max()
        weights.name = "weights"
        sst_anom_weighted = sst_anom.weighted(weights)
        sst_anom_wmean = sst_anom_weighted.mean(("lon", "lat"),skipna=True)

    ## Save in netcdf
        print('    > Save to netcdf')
        sst_wmean.to_netcdf(dataDir+'/sstd_mean_'+titulo_short+'.nc',mode='w')
        sst_anom_wmean.to_netcdf(dataDir+'/sstd_anom_mean_'+titulo_short+'.nc',mode='w')

        sst_anom_LD=sst_anom[-1,:,:]
        sst_anom_LD.to_netcdf(dataDir+'/sstLD_anom_'+titulo_short+'.nc',mode='w')
        
    # Monthly analisis
        #print('>>>>> Monthly')
        #sst = sst.resample(time='ME').mean(dim='time',skipna=True)

    ## Calculate global mean weigthtened
        #print('    > Compute weigthtened mean')
        #weights = np.cos(np.deg2rad(sst.lat))
        #weights = weights/weights.max()
        #weights.name = "weights"
        #sst_weighted = sst.weighted(weights)
        #sst_wmean = sst_weighted.mean(("lon", "lat"),skipna=True)
        
    ## Create monthly climatology
        #print('    > create climatology')
        #sst_clim = sst.sel(time=slice(yearC1,yearC2)).groupby('time.month').mean(dim='time');
    ## Create anomaly
        #print('    > Compute anomaly mean')
        #sst_anom = sst.groupby('time.month') - sst_clim

    ##Calculate global mean weigthtened
        #print('    > Compute weigthtened mean')
        #weights = np.cos(np.deg2rad(sst.lat))
        #weights = weights/weights.max()
        #weights.name = "weights"
        #sst_anom_weighted = sst_anom.weighted(weights)
        #sst_anom_wmean = sst_anom_weighted.mean(("lon", "lat"),skipna=True).load()
        
    ##Save in netcdf
        #print('    > to netcdf')
        #sst_anom.to_netcdf(dataDir+'/sstm_anom_'+titulo_short+'.nc',mode='w')
        #sst_wmean.to_netcdf(dataDir+'/sstm_mean_'+titulo_short+'.nc',mode='w')
        #sst_anom_wmean.to_netcdf(dataDir+'/sstm_anom_mean_'+titulo_short+'.nc',mode='w')

        print("    > %s seconds ---" % (time.time() - start_time))
#---------------------------------------------------------------------<<<<
#         
if __name__ == '__main__':
    cluster = LocalCluster(n_workers=20, threads_per_worker=1)
    client = Client(cluster)
    
    print('>>>>> analysisDataDemarcaciones' )
    
    start_time = time.time()
    
    funcionPrincipal()
    
    cluster.close()
    client.close()

    print('      analysisDataDemarcaciones %6.0f s<<<<<' % (time.time() - start_time))
