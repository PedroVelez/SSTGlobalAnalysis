from ftplib import FTP
import datetime
import os

from globales import *
# ------------------------------------------------------------------------
# Inicio
# ------------------------------------------------------------------------
print('>>>>> downloadData' )

data_dir = GlobalSU['DatPath'] + '/Satelite/noaa.oisst.v2.highres/NC'

year = datetime.date.today().year
fileThisYear = 'sst.day.mean.'+str(year)+'.nc'

os.chdir(data_dir)

print('    > Downloading data '+fileThisYear+' in '+data_dir)
    
ftp = FTP('ftp.cdc.noaa.gov')  # connect to host, default port
ftp.login()  
ftp.cwd('Datasets/noaa.oisst.v2.highres/');

ftp.retrbinary("RETR " + fileThisYear, open(fileThisYear, 'wb').write)
ftp.quit()

print('    > Downloaded data '+fileThisYear+' in '+data_dir)

DS = xr.open_dataset(data_dir+'/'+fileThisYear)
print('    > Last data: '+DS.time[-1].dt.strftime("%d %B %Y").values)

print('      downloadData <<<<<' )
