from globales import *

import smtplib
from email.message import EmailMessage
from email.utils import formataddr

import numpy as np
import xarray as xr
import pandas as pd
from matplotlib.dates import DateFormatter

import datetime

import os
import math

from dotenv import load_dotenv

import locale 

locale.setlocale(locale.LC_TIME, "es_ES");

# ------------------------------------------------------------------------
# Inicio
# ------------------------------------------------------------------------
print('>>>>> sendReportGlobal' )

# Funciones --------------------------------------------------------------
def ReportSerieTemporal(sst):
## Serie temporal anotada con valores maximos y minimos
    
    sst_rolling = sst.rolling(time = 360 , center = True).mean()
    
    tmax = sst.isel(sst.argmax(...))
    tmin = sst.isel(sst.argmin(...))
    
    d_tmax = sst.time.isel(sst.argmax(...))
    d_tmin = sst.time.isel(sst.argmin(...))
    
    #Linear fit
    ind = np.isfinite(sst)
    z = np.polyfit(sst.time.astype(np.int64)[ind],sst[ind], 1)
    Dlinearf = z[0] * sst.time.astype(np.int64) + z[1]
    Dslope=z[0]/1.e-9*24*3600*365*100 #paso a C por siglo
    tTendencia =  "Incremento \n %2.2f C "%(sst[-1]-sst[0]) + ' desde el ' + sst.time[0].dt.strftime("%d %B %Y").values + " (Tendencia: " + "%2.2f"%(Dslope) + " C/siglo )"

    tTActual = sst.time[-1].dt.strftime("%d %B %Y").values + " %2.2f $^\circ$C "%(sst[-1].values)
    tTMaxima =  'Temperatura máxima: ' + "%2.2f ºC"%(tmax) + ' el ' + d_tmax.dt.strftime("%d %B %Y").values+ '. '
    tTMinima =  'Temperatura mínima: ' + "%2.2f ºC"%(tmin) + ' el ' + d_tmin.dt.strftime("%d %B %Y").values+ '. '
    tPeriodo =  " [" + sstd.time[0].dt.strftime("%d %B %Y").values + " - "+ sstd.time[-1].dt.strftime("%d %B %Y").values + "]"
    
    texto = tTMaxima + tTMinima + tTendencia
    return texto

def ReportSerieTemporal_anual(sst,TituloFigura):
# Serie temporal por años    

    currentYear = datetime.date.today().year
    sstHist = sst.sel(time=slice("1982-01-01", str(currentYear-1)+"-12-31"))

    df         = sstHist.groupby(sstHist.time.dt.dayofyear).mean().to_dataframe(name="mean")
    df["std"]  = sstHist.groupby(sstHist.time.dt.dayofyear).std().values

    for year, yearda in sst.groupby(sst.time.dt.year):
        df[year] = pd.Series(index=yearda["time"].dt.dayofyear, data=yearda.values)
    
    df.index   = pd.date_range(start='01/Jan/2020', end='31/12/2020', freq='D')  

    currentYear = datetime.date.today().year
    indLastData = np.where(df[currentYear].isnull())[0].tolist()[0]-1

    date_form = DateFormatter("1-%b")
    
    tTActual = sst.time[-1].dt.strftime("%d %B %Y").values + " %2.2f (C) "%(sst[-1].values)+ '. '

    texto=TituloFigura + tTActual
    return texto
# -----------------------------------------------------------------------

## Read env data
load_dotenv()

SOURCE_IMAP = os.getenv("SOURCE_IMAP")
SOURCE_SMTP = os.getenv("SOURCE_SMTP")
ARGO_USER   = os.getenv("ARGO_USER")
ARGO_MAIL   = os.getenv("ARGO_MAIL")
ARGO_PASS   = os.getenv("ARGO_PASS")

Titulos = ['Oceano Global','Hemisferio norte','Hemisferio sur','AtlanticoNorte', 'Demarcación marina levantino-balear', 'Demarcación marina noratlántica','Demarcación marina canaria','Demarcación sudatlántica','Demarcación Estrecho y Alborán','Iberian Canary Basin']
Titulos_short = ['GO','NH','SH','NAtl','LEB', 'NOR','CAN','SUD','ESA','IBICan']

analisisDir   = GlobalSU['AnaPath'] + '/SSTGlobalAnalysis'
dataDir   = GlobalSU['AnaPath'] + '/SSTGlobalAnalysis/data'

# Daily data
it=0

titulo = Titulos[it]
titulo_short = Titulos_short[it]

data = xr.open_dataset(dataDir+'/sstd_mean_'+titulo_short+'.nc')
sstd = data.sst
data = xr.open_dataset(dataDir+'/sstd_anom_mean_'+titulo_short+'.nc')
sstd_anom = data.sst

Title1  = '- SST en el '+ titulo +'. '
texto1 = ReportSerieTemporal_anual(sstd,Title1)
texto2 = ReportSerieTemporal(sstd)

Title2  = '- Anomalía SST (respecto del periodo 1982-1992), en el '+ titulo+'. '
texto3 = ReportSerieTemporal_anual(sstd_anom,Title2)
texto4 = ReportSerieTemporal(sstd_anom)


current_date = datetime.datetime.now().strftime('%d-%b-%Y %H:%M:%S')

msg = EmailMessage()
msg['Subject'] = 'Global Analisis SST '+current_date
msg['From'] = formataddr(("IEOOS", ARGO_MAIL))
msg['To'] = 'pvelezbelchi@gmail.com'
msg.add_alternative(f"""
<html>
  <body>
    <p>{texto1}</p>
    <p>{texto2}</p>
    <p>{texto3}</p>
    <p>{texto4}</p>
    <p><a href="https://www.oceanografia.es/pedro/research_SST_GLOBAL.html">Global SST Analysis</a></p>
  </body>
</html>
""", subtype='html')

# Attach an image
with open(analisisDir+'/images/map_sstd_anom_GO.png', 'rb') as img:
    img_data = img.read()
    msg.add_attachment(img_data, maintype='image', subtype='png', filename='map_sstd_anom_GO.png')

with open(analisisDir+'/images/map_sstd_anom_NAtl.png', 'rb') as img:
    img_data = img.read()
    msg.add_attachment(img_data, maintype='image', subtype='png', filename='map_sstd_anom_NAtl.png')

with open(analisisDir+'/images/sstd_GO.png', 'rb') as img:
    img_data = img.read()
    msg.add_attachment(img_data, maintype='image', subtype='png', filename='sstd_GO.png')

with open(analisisDir+'/images/sstd_anom_mean_GO_HN_HS.png', 'rb') as img:
    img_data = img.read()
    msg.add_attachment(img_data, maintype='image', subtype='png', filename='sstd_anom_mean_GO_HN_HS.png')

with open(analisisDir+'/images/sstd_anom_mean_NAtl.png', 'rb') as img:
    img_data = img.read()
    msg.add_attachment(img_data, maintype='image', subtype='png', filename='sstd_anom_mean_NAtl.png')

with open(analisisDir+'/images/sstd_anom_NAtl.png', 'rb') as img:
    img_data = img.read()
    msg.add_attachment(img_data, maintype='image', subtype='png', filename='sstd_anom_NAtl.png')

# Send the email
with smtplib.SMTP_SSL(SOURCE_SMTP, 465) as smtp:
    smtp.login(ARGO_USER, ARGO_PASS)
    smtp.send_message(msg)



