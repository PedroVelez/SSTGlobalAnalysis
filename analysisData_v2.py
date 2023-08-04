# Global mean Sea Surface Temperatures
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pandas as pd
from matplotlib.dates import DateFormatter
import os

# Settings compute de climatoloy
year1='1982'
year2='1992'

Titulos = ['AtlanticoNorte']
Titulos_short = ['NAtl']


# Load data
if os.uname().nodename.lower().find('eemmmbp') != -1:
    base_file = '/Users/pvb/Dropbox/Oceanografia/Data/Satelite/noaa.oisst.v2.highres/NC/sst.day.mean'
elif os.uname().nodename.lower().find('rossby') != -1:
    base_file = '/data/shareddata/Satelite/noaa.oisst.v2.highres/NC/sst.day.mean'
    dataDir = '/home/pvb/Analisis/SSTGlobalAnalysis/data'

f = open("/home/pvb/Analisis/SSTGlobalAnalysis/prueba.log", "a")
print('>>>>> Cargando ficheros de '+base_file)
f.write('>>>>> Cargando ficheros de '+base_file)
files = [f'{base_file}.{year}.nc' for year in range(1982, 2024)]
DS = xr.open_mfdataset(files)

f.close()

