import platform
import os

import numpy as np
import xarray as xr
import pandas as pd

from dask.distributed import Client
from dask import delayed
import dask

from calendar import monthrange

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

import cartopy.crs as ccrs
import cartopy
import cartopy.feature as cfeature

from shapely.geometry import Polygon, Point
from shapely.ops import transform
import pyproj

from globales import *

base_file = GlobalSU['DatPath'] + '/Satelite/MUR/NC/'
dataDir   = GlobalSU['AnaPath']  + '/SSTGlobalAnalysis/data'

year1= 2003
year2= 2013
files = []
for iy in range(year1,year2+1):
    for im in range(1,13):
        for id in range(1,monthrange(iy,im)[1]+1):
            files.append(base_file+"%04d%02d%02d090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc"%(iy,im,id))

DS = xr.open_mfdataset(files)
sst1=DS.analysed_sst.sel(lat=29,lon=-15).load()
sst1.to_netcdf(dataDir+'/sst1.nc',mode='w')


