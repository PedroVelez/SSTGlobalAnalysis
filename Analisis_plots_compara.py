import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pandas as pd
from matplotlib.dates import DateFormatter
import datetime
import os

plt.rcParams['figure.figsize'] = (10, 4)

# Daily data
data = xr.open_dataset('./data/sstd_anom_mean_GO.nc')
sstdGO_anom = data.sst
data = xr.open_dataset('./data/sstd_anom_mean_NH.nc')
sstdNH_anom = data.sst
data = xr.open_dataset('./data/sstd_anom_mean_SH.nc')
sstdSH_anom = data.sst

sstdSH_anom_rolling = sstdSH_anom.rolling(time = 360 , center = True).mean()
sstdNH_anom_rolling = sstdNH_anom.rolling(time = 360 , center = True).mean()
sstdGO_anom_rolling = sstdGO_anom.rolling(time = 360 , center = True).mean()

fileOut = './images/sstd_anom_GO_HN_HS.png'

fig,ax = plt.subplots(figsize=(14,8))
ax.plot(sstdNH_anom_rolling.time,sstdNH_anom_rolling,'r',label='Hemisferio norte',linewidth=3)
#ax.plot(sstdNH_anom.time,sstdNH_anom,'r',linewidth=1,alpha=0.6)
ax.plot(sstdSH_anom_rolling.time,sstdSH_anom_rolling,'c',label='Hemisferio sur',linewidth=3)
#ax.plot(sstdSH_anom.time,sstdSH_anom,'c',linewidth=1,alpha=0.6)
ax.plot(sstdGO_anom_rolling.time,sstdGO_anom_rolling,'b',label='Oceano global',linewidth=4)
ax.plot(sstdGO_anom.time,sstdGO_anom,'b',linewidth=1,alpha=0.6)


tmax = sstdGO_anom.isel(sstdGO_anom.argmax(...))
tmin = sstdGO_anom.isel(sstdGO_anom.argmin(...))
d_tmax = sstdGO_anom.time.isel(sstdGO_anom.argmax(...))
d_tmin = sstdGO_anom.time.isel(sstdGO_anom.argmin(...))
    
ax.plot(d_tmax , tmax,'rs' , markersize = 12 , markeredgecolor='k')
ax.plot(d_tmin , tmin,'bs' , markersize = 12 , markeredgecolor='k')

ax.legend(loc = 4)
ax.grid(linestyle=':', linewidth=.5)

ax.set_ylabel('Temperatura [ºC]')
ax.set_xlabel('Fecha')
TituloFigura='Promedio de anomalia de temperatura superficial. Anomalia respecto de 1982-1992'
ax.set_title(TituloFigura + '\n' + 
        sstdGO_anom.time[-1].dt.strftime("%d %B %Y").values + "%2.3f ºC "%(sstdGO_anom[-1].values) + '\n' + 
        'Temperatura maxima global: ' + "%2.3f ºC"%(sstdGO_anom.isel(sstdGO_anom.argmax(...)).values) +
        ' (' + sstdGO_anom.time.isel(sstdGO_anom.argmax(...)).dt.strftime("%d %B %Y").values + ')' + '\n' +
        'Periodo ['+sstdGO_anom.time[0].dt.strftime("%d %B %Y").values + " - "+ sstdGO_anom.time[-1].dt.strftime("%d %B %Y").values + ']');
plt.savefig(fileOut)