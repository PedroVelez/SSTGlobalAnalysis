import numpy as np
import xarray as xr
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.dates import DateFormatter

import cartopy.crs as ccrs
import cartopy
import cartopy.feature as cfeature
plt.rcParams['figure.figsize'] = (10, 4)

import time
import datetime
import os

import locale 
locale.setlocale(locale.LC_TIME, "es_ES");

from globales import *
# ------------------------------------------------------------------------
# Inicio
# ------------------------------------------------------------------------
print('>>>>> plotsMapAnomaliesDemarcaciones' )
start_time = time.time()

analisisDir   = GlobalSU['AnaPath'] + '/SSTGlobalAnalysis'

Titulos = ['Demarcación marina levantino-balear', 'Demarcación marina noratlántica','Demarcación marina canaria','Demarcación sudatlántica','Demarcación Estrecho y Alborán','Iberian Canary Basin']
Titulos_short = ['LEB', 'NOR','CAN','SUD','ESA','IBICan']

for i in range(0,len(Titulos)):
    titulo = Titulos[i]
    titulo_short = Titulos_short[i]

    Title  = 'Anomalía de temperatura superficial, respecto de 1982-1992, en la '+ titulo
    FileIn =  analisisDir+'/data/sstLD_anom_'+titulo_short+'.nc'
    FileOut = analisisDir+'/images/map_sstd_anom_'+titulo_short+'.png'
    
    print('    > '+Title)
    
    data = xr.open_dataset(FileIn)
    sst = data.sst

    escalaLand='50m'

# Load the data from the .txt file
    lon, lat = [], []
    if titulo_short == 'CAN' or titulo_short == 'ESA' or titulo_short ==  'LEB' or titulo_short ==  'NOR' or titulo_short ==  'SUD' :
        with open(analisisDir+'/data/Demarcacion'+titulo_short+'.txt', 'r') as f:
            for line in f:
                longitude, latitude = map(float, line.split())
                lon.append(longitude)
                lat.append(latitude)
            
    ## Figura
    fig = plt.figure(figsize=(14,8))

    ax = plt.axes(projection=ccrs.Mollweide(),frameon=False)
    ax.patch.set_visible(False)

    land = cartopy.feature.NaturalEarthFeature('physical', 
                'land', edgecolor='k', scale = escalaLand ,
                facecolor=cfeature.COLORS['land'])
    ax.add_feature(land, facecolor='beige')
    
    cm=ax.contourf(sst.lon,sst.lat,sst, levels=np.arange(-4,4.1,0.25), 
               transform=ccrs.PlateCarree(),
               cmap = plt.cm.RdBu.reversed(),
               vmin = -4,vmax = 4,extend='both')

    cl = ax.contour(sst.lon,sst.lat,sst, levels=[0],
                           colors='black', linewidths=1,
                           transform=ccrs.PlateCarree())

    ax.clabel(cl, inline=True, fontsize=8, fmt="%1.1f")

    ax.plot(lon, lat, transform=ccrs.PlateCarree())

    cbar=fig.colorbar(cm,ax=ax, location='right',
                  shrink=.8, ticks=[-4,-2,0,2,4], 
                  drawedges=True)

    gd=ax.gridlines(draw_labels=True, linewidth=.5, color='gray', alpha=0.5, linestyle='--',x_inline=False, y_inline=False)
    gd.ylocator = mticker.FixedLocator([25, 35, 45])
    gd.xlocator = mticker.FixedLocator([-30, -20, -10,0])
    gd.left_labels = False
    gd.top_labels = False


    ax.set_title(Title + ', ' + sst.time.dt.strftime("%d %B %Y").values + '\n');

    plt.savefig(FileOut)

print('      plotsMapAnomaliesDemarcaciones %6.0f s<<<<<' % (time.time() - start_time))

