from ftplib import FTP
import datetime
import os
import xarray as xr

from globales import *
# ------------------------------------------------------------------------
# Inicio
# ------------------------------------------------------------------------
HOME=os.environ['HOME']   
f = open(HOME+'/.env', 'r')
for line in f.readlines():
    Name=line.strip().split('=')[0]
    Content=line.strip().split('=')[-1]
    if Name=='dirData' or Name=='dirAnalisis':
        exec(Name + "=" + "'" + Content + "'")
f.close()

data_dir = GlobalSU['DatPath'] + '/Satelite/noaa.oisst.v2.highres/NC'

year = datetime.date.today().year
fileThisYear = 'sst.day.mean.'+str(year)+'.nc'

os.chdir(data_dir)

print('>>>>> Downloading data '+fileThisYear+' in '+data_dir)
    
ftp = FTP('ftp.cdc.noaa.gov')  # connect to host, default port
ftp.login()  
ftp.cwd('Datasets/noaa.oisst.v2.highres/');

ftp.retrbinary("RETR " + fileThisYear, open(fileThisYear, 'wb').write)
ftp.quit()

print('>>>>> Downloaded data '+fileThisYear+' in '+data_dir)

DS = xr.open_dataset(data_dir+'/'+fileThisYear)
print('>>>>> Last data: '+DS.time[-1].dt.strftime("%d %B %Y").values)
