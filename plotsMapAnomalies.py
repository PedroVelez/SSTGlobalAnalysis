import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pandas as pd
from matplotlib.dates import DateFormatter
import datetime
import os

import cartopy.crs as ccrs
import cartopy
import cartopy.feature as cfeature

plt.rcParams['figure.figsize'] = (10, 4)

if os.uname().nodename.lower().find('eemmmbp') != -1:
    imagesDir = '/home/pvb/Dropbox/Oceanografia/Analisis/SSTGlobalAnalysis/images'
elif os.uname().nodename.lower().find('rossby') != -1:
    imagesDir = '/home/pvb/Analisis/SSTGlobalAnalysis/images'
    dataDir = '/home/pvb/Analisis/SSTGlobalAnalysis/data'

Titulos = ['Oceano Global','AtlanticoNorte']
Titulos_short = ['GO','NAtl']

for i in range(0,len(Titulos)):
    titulo = Titulos[i]
    titulo_short = Titulos_short[i]

    Title  = 'Anomalia de temperatura superficial en el '+ titulo
    FileIn =  './data/sstLD_anom_'+titulo_short+'.nc'
    FileOut = './images/map_sstd_anom_'+titulo_short+'.png'
    
    print('>>>>> '+Title)
    
    data = xr.open_dataset(FileIn)
    sst = data.sst

## Figura
    fig = plt.figure(figsize=(14,8))
    ax = plt.axes(projection=ccrs.Robinson())

    land = cartopy.feature.NaturalEarthFeature('physical', 
                'land', edgecolor='k', scale = '110m' ,
                facecolor=cfeature.COLORS['land'])

    ax.add_feature(land, facecolor='beige')
    ax.add_feature(cfeature.LAND)
    
    cm=ax.contourf(sst.lon,sst.lat,sst, levels=np.arange(-4,4.1,0.25), 
               transform=ccrs.PlateCarree(),
               cmap = plt.cm.RdBu.reversed(),
               vmin = -4,vmax = 4,extend='both')

    cbar=fig.colorbar(cm,ax=ax, location='bottom',
                  shrink=.8, ticks=[-4,-2,0,2,4], 
                  drawedges=True)

    ax.gridlines(draw_labels=True, linewidth=.5, 
             color='gray', alpha=0.5, linestyle='--')

    ax.set_title(Title + '\n' +
             sst.time.dt.strftime("%d %B %Y").values);

    plt.savefig(FileOut)