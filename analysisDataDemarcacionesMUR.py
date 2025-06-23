# Global mean Sea Surface Temperatures
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pandas as pd

from calendar import monthrange

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
    base_file = GlobalSU['DatPath'] + '/Satelite/MUR/NC/'
    dataDir   = GlobalSU['AnaPath'] + '/SSTGlobalAnalysis/data'
    imagesDir = GlobalSU['AnaPath'] + '/SSTGlobalAnalysis/images'

    # Settings 
    year1=2003
    year2=2025

    # Settings compute de climatoloy
    yearC1='2003'
    yearC2='2012'

    Titulos = ['Demarcación marina canaria','Demarcación marina levantino-balear', 'Demarcación marina noratlántica','Demarcación sudatlántica','Demarcación Estrecho y Alborán','Iberian Canary Basin']
    Titulos_short = ['CAN','LEB', 'NOR','SUD','ESA','IBICan']

    # Load data
    print('>>>>> Cargando ficheros de '+base_file)

    files = []
    for iy in range(year1,year2):
        for im in range(1,13):
            for id in range(1,monthrange(iy,im)[1]+1):
                files.append(base_file+"%04d%02d%02d090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc"%(iy,im,id))
    iy=year2
    for im in range(1,6):
        for id in range(1,monthrange(iy,im)[1]+1):
            files.append(base_file+"%04d%02d%02d090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc"%(iy,im,id))
    iy=year2
    im=6
    for id in range(1,16):
        files.append(base_file+"%04d%02d%02d090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc"%(iy,im,id))

    def drop_coords(ds):
        ds = ds.get(['analysed_sst'])
        return ds.reset_coords(drop=True)

    DS = xr.open_mfdataset(files,combine='nested', concat_dim="time", parallel=True, combine_attrs= "drop", preprocess=drop_coords,autoclose = True, data_vars='minimal', coords="minimal")        

    # For each demarcacion
    for i in range(0,len(Titulos)):

        titulo = Titulos[i]
        titulo_short = Titulos_short[i]
        start_time = time.time()
        
        demCoord = []
        longDem, latiDem = [], []
        with open(dataDir+'/Demarcacion'+titulo_short+'.txt', 'r') as f:
            for line in f:
            # Split the line by whitespace and append the values
                longitude, latitude = map(float, line.split())
                longitude=longitude
                longDem.append(longitude)
                latiDem.append(latitude)
                demCoord.append((longitude,latitude))
        demPolygon = Polygon(demCoord)    
        demPolygon_transformed = transform_polygon(demPolygon)

        # Select the data for the demarcacion
        if titulo_short == 'LEB':
            slicelatitude=slice(35.5,42.75)
            slicelongitude=slice(358-360,8)
            sst=DS.analysed_sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
            mask = np.array([[point_in_polygon(lon,lat,demPolygon_transformed) 
            for lon in sst.lon.values] 
            for lat in sst.lat.values])
            sst_unmasked = sst
            sst = sst.where(mask)
            print('>>>>> '+titulo) 
    

        elif  titulo_short == 'NOR':
            slicelatitude=slice(41.25,47)
            slicelongitude=slice(345-360,360-360)
            sst=DS.analysed_sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
            mask = np.array([[point_in_polygon(lon,lat,demPolygon_transformed) 
            for lon in sst.lon.values] 
            for lat in sst.lat.values])
            sst_unmasked = sst
            sst = sst.where(mask)
            print('>>>>> '+titulo)        
            
        elif  titulo_short == 'CAN':
            slicelatitude=slice(24,32.5)
            slicelongitude=slice(335-360,350-360)
            sst=DS.analysed_sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
            mask = np.array([[point_in_polygon(lon,lat,demPolygon_transformed) 
            for lon in sst.lon.values] 
            for lat in sst.lat.values])
            sst_unmasked = sst
            sst = sst.where(mask)
            print('>>>>> '+titulo)    

        elif  titulo_short == 'SUD':
            slicelatitude=slice(35.5,37.5)
            slicelongitude=slice(352-360,354.5-360)
            sst=DS.analysed_sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
            mask = np.array([[point_in_polygon(lon,lat,demPolygon_transformed) 
            for lon in sst.lon.values] 
            for lat in sst.lat.values])
            sst_unmasked = sst
            sst = sst.where(mask)
            print('>>>>> '+titulo)

        elif  titulo_short == 'ESA':
            slicelatitude=slice(35.5,37)
            slicelongitude=slice(354-360,358.5-360)
            sst=DS.analysed_sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
            mask = np.array([[point_in_polygon(lon,lat,demPolygon_transformed) 
            for lon in sst.lon.values] 
            for lat in sst.lat.values])
            sst_unmasked = sst
            sst = sst.where(mask)
            print('>>>>> '+titulo)
        elif  titulo_short == 'IBICan':
            sst = DS.analysed_sst.sel(lat=slice(20, 47),lon=slice(325-360,360-360))
            # Para blanquear el mediterraneo
            lat_point_list = [40, 40, 30, 30, 40]
            lon_point_list = [354.5-360, 360-360, 360-360, 354.5-360, 354.5-360]
            polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
            polygon = transform_polygon(polygon_geom)
            mask = np.array([[point_in_polygon(lon,lat,polygon) 
                    for lon in sst.lon.values] 
                    for lat in sst.lat.values])
            
            sst = sst.where(~mask)
            print('>>>>> '+titulo)

    # Convert to Celsius
        sst=sst-273.15
        sst = sst.chunk({"time":1, "lat":sst.sizes['lat'], "lon":sst.sizes['lon']})
    
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
        sst_wmean.to_netcdf(dataDir+'/sstdMUR_mean_'+titulo_short+'.nc',mode='w')
        sst_anom_wmean.to_netcdf(dataDir+'/sstdMUR_anom_mean_'+titulo_short+'.nc',mode='w')

        sst_anom_LD=sst_anom[-1,:,:]
        sst_anom_LD.to_netcdf(dataDir+'/sstLDMUR_anom_'+titulo_short+'.nc',mode='w')

        print("    > %s seconds ---" % (time.time() - start_time))
#---------------------------------------------------------------------<<<<
#         
if __name__ == '__main__':
    cluster = LocalCluster(n_workers=26, threads_per_worker=1)
    client = Client(cluster)
    
    print('>>>>> analysisDataMURDemarcaciones' )
    
    start_time = time.time()
    
    funcionPrincipal()
    
    cluster.close()
    client.close()

    print('      analysisDataDemarcaciones %6.0f s<<<<<' % (time.time() - start_time))
