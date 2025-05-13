import numpy as np
import xarray as xr
import pandas as pd

from calendar import monthrange
import time

from shapely.geometry import Polygon, Point
from shapely.ops import transform
import pyproj

from globales import *

from FuncionesArea import *

import multiprocessing
from dask.distributed import Client, LocalCluster

# ------------------------------------------------------------------------
# Inicio
# ------------------------------------------------------------------------
def funcionPrincipal():
    
    # Funciones --------------------------------------------------------------
    #def transform_polygon(polygon, src_crs='epsg:4326', tgt_crs='epsg:4326'):
    #    proj = pyproj.Transformer.from_proj(pyproj.Proj(src_crs), pyproj.Proj(tgt_crs), always_xy=True)
    #    return transform(lambda x, y: proj.transform(x, y), polygon)

    #def point_in_polygon(lon, lat, polygon):
    #    point = Point(lon, lat)
    #    return polygon.contains(point)
    #---------------------------------------------------------------------<<<<

    year1= 2003
    year2= 2024

    # Settings compute de climatoloy
    yearC1='2003'
    yearC2='2024'

    base_file = GlobalSU['DatPath'] + '/Satelite/MUR/NC/'
    dataDir   = GlobalSU['AnaPath'] + '/SSTGlobalAnalysis/data'
    imagesDir = GlobalSU['AnaPath'] + '/SSTGlobalAnalysis/images'

    Titulos = ['Iberian Canary Basin','Demarcación marina levantino-balear', 'Demarcación marina noratlántica','Demarcación marina canaria','Demarcación sudatlántica','Demarcación Estrecho y Alborán']
    Titulos_short = ['IBICan','LEB', 'NOR','CAN','SUD','ESA']

    files = []
    for iy in range(year1,year2+1):
        for im in range(1,13):
            for id in range(1,monthrange(iy,im)[1]+1):
                    files.append(base_file+"%04d%02d%02d090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc"%(iy,im,id))

    def drop_coords(ds):
        ds = ds.get(['analysed_sst'])   
        return ds.reset_coords(drop=True)

    print('   >> Cargando ficheros de '+base_file)

    DS = xr.open_mfdataset(files,combine='nested', concat_dim="time", parallel=True, combine_attrs= "drop", preprocess=drop_coords,autoclose = True, data_vars='minimal', coords="minimal")
        
    for it in range(1,6):
        start_time = time.time()
        
        titulo = Titulos[it]
        titulo_short = Titulos_short[it]
        
        # Load the data from the .txt file
        demCoord = []
        longDem, latiDem = [], []
        with open('./data/Demarcacion'+titulo_short+'.txt', 'r') as f:
            for line in f:
                # Split the line by whitespace and append the values
                longitude, latitude = map(float, line.split())
                longitude=longitude
                longDem.append(longitude)
                latiDem.append(latitude)
                demCoord.append((longitude,latitude))
            demPolygon = Polygon(demCoord)    
            demPolygon_transformed = transform_polygon(demPolygon)

        # Recorta map
        if titulo_short == 'LEB':
            slicelatitude=slice(35.5,42.75)
            slicelongitude=slice(358,368)
            sst=DS.analysed_sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
            mask = np.array([[point_in_polygon(lon,lat,demPolygon_transformed) 
                for lon in sst.lon.values] 
                for lat in sst.lat.values])
            sst_unmasked = sst
            sst = sst.where(mask)
            print('   >> '+titulo)        

        elif  titulo_short == 'NOR':
            slicelatitude=slice(41.5,46.9)
            slicelongitude=slice(346,360)
            sst=DS.analysed_sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
            mask = np.array([[point_in_polygon(lon,lat,demPolygon_transformed) 
                for lon in sst.lon.values] 
                for lat in sst.lat.values])
            sst_unmasked = sst
            sst = sst.where(mask)
            print('   >> '+titulo)              
                
        elif  titulo_short == 'CAN':
            slicelatitude=slice(24,32.5)
            slicelongitude=slice(335-360,350-360)
            sst=DS.analysed_sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
            mask = np.array([[point_in_polygon(lon,lat,demPolygon_transformed) 
                for lon in sst.lon.values] 
                for lat in sst.lat.values])
            sst_unmasked = sst
            sst = sst.where(mask)
            print('   >> '+titulo)           

        elif  titulo_short == 'SUD':
            slicelatitude=slice(35.5,37.5)
            slicelongitude=slice(352,354.5)
            sst=DS.analysed_sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
            mask = np.array([[point_in_polygon(lon,lat,demPolygon_transformed) 
                for lon in sst.lon.values] 
                for lat in sst.lat.values])
            sst_unmasked = sst
            sst = sst.where(mask)
            print('   >> '+titulo)        

        elif  titulo_short == 'ESA':
            slicelatitude=slice(35.5,37)
            slicelongitude=slice(354,358.5)
            sst=DS.analysed_sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
            mask = np.array([[point_in_polygon(lon,lat,demPolygon_transformed) 
                for lon in sst.lon.values] 
                for lat in sst.lat.values])
            sst_unmasked = sst
            sst = sst.where(mask)
            print('   >> '+titulo)        

        elif  titulo_short == 'IBICan':
            sst = DS.analysed_sst.sel(lat=slice(20, 47),lon=slice(325,360))
            # Para blanquear el mediterraneo
            lat_point_list = [40, 40, 30, 30, 40]
            lon_point_list = [354.5, 360, 360, 354.5, 354.5]
            polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
            polygon = transform_polygon(polygon_geom)
            mask = np.array([[point_in_polygon(lon,lat,polygon) 
                        for lon in sst.lon.values] 
                        for lat in sst.lat.values])  
            sst = sst.where(~mask)
            print('   >> '+titulo)         

        #sst = sst.chunk({"time":1, "lat":851, "lon":1501})

        # Daily analisis
        print('   >> Daily'+titulo+titulo_short)

        ## Calculate mean weigthtened
        weights = np.cos(np.deg2rad(sst.lat))
        weights = weights/weights.max()
        weights.name = "weights"
        sst_weighted = sst.weighted(weights)
        sst_wmean = sst_weighted.mean(("lon", "lat"),skipna=True)

        ## Create monthly climatology
        sst_clim = sst.sel(time=slice(yearC1,yearC2)).groupby('time.dayofyear').mean(dim='time')

        ## Create anomaly
        sst_anom = sst.groupby('time.dayofyear') - sst_clim

        ## Calculate global mean anomaly
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

        # Monthly analisis
        sst = sst.resample(time='ME').mean(dim='time',skipna=True)

        ## Calculate global mean weigthtened
        weights = np.cos(np.deg2rad(sst.lat))
        weights = weights/weights.max()
        weights.name = "weights"
        sst_weighted = sst.weighted(weights)
        sst_wmean = sst_weighted.mean(("lon", "lat"),skipna=True)
            
        ## Create monthly climatology
        sst_clim = sst.sel(time=slice(yearC1,yearC2)).groupby('time.month').mean(dim='time');

        ## Create anomaly
        print('    > Compute anomaly mean')
        sst_anom = sst.groupby('time.month') - sst_clim
    
        ##Calculate global mean weigthtened
        print('    > Compute weigthtened mean')
        weights = np.cos(np.deg2rad(sst.lat))
        weights = weights/weights.max()
        weights.name = "weights"
        sst_anom_weighted = sst_anom.weighted(weights)
        sst_anom_wmean = sst_anom_weighted.mean(("lon", "lat"),skipna=True)
        
        ##Save in netcdf
        print('    > to netcdf')
        sst_anom.to_netcdf(dataDir+'/sstmMUR_anom_'+titulo_short+'.nc',mode='w')
        sst_wmean.to_netcdf(dataDir+'/sstmMUR_mean_'+titulo_short+'.nc',mode='w')
        sst_anom_wmean.to_netcdf(dataDir+'/sstmMUR_anom_mean_'+titulo_short+'.nc',mode='w')

        print("    > %s seconds ---" % (time.time() - start_time))
#---------------------------------------------------------------------<<<<

if __name__ == '__main__':
    cluster = LocalCluster(n_workers=20, threads_per_worker=1)
    client = Client(cluster)
    
    print('>>>>> analysisDataMUR_Demarcaciones' )
    
    start_time = time.time()
    
    funcionPrincipal()
    
    cluster.close()
    client.close()

    print("--- %s seconds ---" % (time.time() - start_time))
