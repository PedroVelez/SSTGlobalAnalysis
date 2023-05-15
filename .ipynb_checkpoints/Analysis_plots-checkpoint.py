import numpy as np
import xarray as xr
import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
matplotlib.use('agg')
import warnings
warnings.filterwarnings("ignore")


Titulos = ['Oceano Global','Hemisferio norte','Hemisferio sur']
Titulos_short = ['GO','NH','SH']

## Funciones
def FiguraSerieTemporal(sst,Ylabel,Xlabel,TituloFigura,FileOut,Ymin,Ymax):
## Serie temporal anotada con valores maximos y minimos

    dTText = .12
    
    sst_rolling = sst.rolling(time = 360 , center = True).mean()
    
    tmax = sst.isel(sst.argmax(...))
    tmin = sst.isel(sst.argmin(...))
    
    d_tmax = sst.time.isel(sst.argmax(...))
    d_tmin = sst.time.isel(sst.argmin(...))
    
    fig, ax = plt.subplots(1 , 1 , figsize = (14,8))
    ax.plot(sst.time , sst,'c' , label = 'Diario')
    #ax.plot(sstm.time,sstm,'g',label='mensual',linewidth='3')
    ax.plot(sst_rolling.time , sst_rolling,'r', label='Suavizado (1 año)' , linewidth = '3')


    ax.plot(d_tmax , tmax,'rs' , markersize = 12 , markeredgecolor='k')
    ax.plot(d_tmin , tmin,'bs' , markersize = 12 , markeredgecolor='k')

    #Texto del maximo
    ax.text(d_tmax , tmax + dTText , 
                d_tmax.dt.strftime("%d %B %Y").values + 
                '\n' + "%2.3f ºC"%(tmax) ,
                horizontalalignment = 'center' , verticalalignment = 'top' ,
                bbox = dict(facecolor = 'white' , alpha=0.5))

    #Texto del minimo
    ax.text(d_tmin , tmin - dTText , 
                d_tmin.dt.strftime("%d %B %Y").values + 
                '\n' + "%2.3f ºC"%(tmin) ,
                horizontalalignment = 'center', verticalalignment = 'top' ,
                bbox = dict(facecolor = 'white', alpha = 0.5))
    ax.grid()
    ax.legend(loc = 4)
    ax.set_ylabel(Ylabel)
    ax.set_xlabel(Xlabel)
    ax.set_title(TituloFigura + '\n' +
             'Max: ' + "%2.3f ºC"%(tmax) +
                 ' (' + d_tmax.dt.strftime("%d %B %Y").values + ')' +
                 ' - ' +
              'Min: ' + "%2.3f ºC"%(tmin) +
                 ' (' + d_tmin.dt.strftime("%d %B %Y").values + ')' + 
                 '\n' +
              "[" + sstd.time[0].dt.strftime("%d %B %Y").values + "-"+ sstd.time[-1].dt.strftime("%d %B %Y").values + "]");
    #ax.set_ylim(Ymin,Ymax)
    plt.savefig(FileOut)
    
#----def FiguraSerieTemporal

def FiguraSerieTemporal_anual(sst,Xlabel,Ylabel,TituloFigura,FileOut,Ymin,Ymax):
# Serie temporal por años    

    dTText = .2
    
    df         = sst.groupby(sst.time.dt.dayofyear).mean().to_dataframe(name="mean")
    df["std"]  = sst.groupby(sst.time.dt.dayofyear).std().values

    for year, yearda in sst.groupby(sst.time.dt.year):
        df[year] = pd.Series(index=yearda["time"].dt.dayofyear,
                             data=yearda.values)
    
    df.index   = pd.date_range(start='01/Jan/2020', end='31/12/2020', freq='D')  

    currentYear = datetime.date.today().year
    indLastData = np.where(df[currentYear].isnull())[0].tolist()[0]-1

    date_form = DateFormatter("1-%b")
    
    #Figura
    fig, ax = plt.subplots(figsize=(14,8))

    ax.plot(df.index,df[currentYear],'b',linewidth='3',label=currentYear)
    for year in range(currentYear-6,1981,-1):
        ax.plot(df.index,df[year],color='#D3D3D3')

    for year in range(currentYear-1,currentYear-6,-1):
        ax.plot(df.index,df[year],label=year)

        
    ax.plot(df.index,df[1982],label='1982')

    ax.plot(df.index[indLastData],df[currentYear][indLastData],'bo', markersize=12)
    ax.plot(df.index,df["mean"],'k',linewidth='3',label='mean')
    ax.fill_between(x=df.index, y1=df["mean"]+2*df["std"], 
                            y2=df["mean"]-2*df["std"],alpha=0.5, color='#D3D3D3',
                            label='1.5*std')


    ax.text(df.index[indLastData], df[currentYear][indLastData] + dTText, 
                '%2.3f ºC '%(sst[-1].values) + ' - ' + sstd.time[-1].dt.strftime("%d %B %Y").values,
                horizontalalignment = 'center' , verticalalignment = 'top' ,
                bbox = dict(facecolor = 'lightgray' , alpha=0.8))

    
    ax.set_xlim(df.index[0],df.index[365])
    ax.xaxis.set_major_formatter(date_form)

    ax.legend()
    ax.grid(linestyle=':', linewidth=.5)

    ax.set_ylabel(Ylabel)
    ax.set_xlabel(Xlabel)
    ax.set_title(TituloFigura + '\n' + 
                 "%2.3f ºC "%(sst[-1].values) + sstd.time[-1].dt.strftime("%d %B %Y").values +
                 '\n' + 
                 'Max: ' + "%2.3f ºC"%(sst.isel(sst.argmax(...)).values) +
                 ' (' + sst.time.isel(sst.argmax(...)).dt.strftime("%d %B %Y").values + ')' + '\n' +
                 '['+sstd.time[0].dt.strftime("%d %B %Y").values + "-"+ sstd.time[-1].dt.strftime("%d %B %Y").values + ']');
    #ax.set_ylim(Ymin,Ymax)
    plt.savefig(FileOut)

#---FiguraSerieTemporal_anual
    
Ylabel  = 'Temperatura[($^\circ$C)]'
Xlabel  = 'Fecha'

## Creo figuras

### Reading data
for i in range(0,len(Titulos)):
    
    titulo = Titulos[i]
    titulo_short = Titulos_short[i]
    
    print('>>>>> Figuras: '+titulo+titulo_short)
    
    # Daily data
    data = xr.open_dataset('./data/sstd_mean_'+titulo_short+'.nc')
    sstd = data.sst
    data = xr.open_dataset('./data/sstd_anom_mean_'+titulo_short+'.nc')
    sstd_anom = data.sst

    # Monthly data
    data = xr.open_dataset('./data/sstm_mean_'+titulo_short+'.nc')
    sstm = data.sst
    data = xr.open_dataset('./data/sstm_anom_mean_'+titulo_short+'.nc')
    sstm_anom = data.sst
    
    ## Times series mean Sea Surface Temperature
    Title1  = 'Temperatura superficial promedio en el '+ titulo
    File1 = './images/sstd_mean_'+titulo_short+'.png'
    FiguraSerieTemporal(sstd,Ylabel,Xlabel,Title1,File1,17.5,19)
    
    ## Times series mean Sea Surface Temperature anomaly 
    Title2  = 'Anomalia de temperatura superficial promedio en el '+ titulo + '\nAnomalia respecto de 1982-1992'
    File2 = './images/sstd_anom_mean_'+titulo_short+'.png'
    FiguraSerieTemporal(sstd_anom,Ylabel,Xlabel,Title2,File2,-0.25,0.8,)
    
    ## Daily times series Sea Surface Temperature
    Title3  = 'Temperatura superficial en el '+ titulo
    File3 = './images/sstd_'+titulo_short+'.png'
    FiguraSerieTemporal_anual(sstd,Ylabel,Xlabel,Title3,File3,17.5,19)

    ## Daily times series anomly Sea Surface Temperature
    Title4  = 'Anomalia de temperatura superficial en el '+ titulo
    File4 = './images/sstd_anom_'+titulo_short+'.png'
    FiguraSerieTemporal_anual(sstd_anom,Ylabel,Xlabel,Title4,File4,-0.25,0.8)