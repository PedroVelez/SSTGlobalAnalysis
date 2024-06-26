from ftplib import FTP
import datetime
import os
import xarray as xr

if os.uname().nodename.lower().find('eemmmbp') != -1:
    data_dir = '/Users/pvb/Dropbox/Oceanografia/Data/Satelite/noaa.oisst.v2.highres/NC'
elif os.uname().nodename.lower().find('sagams') != -1:
    data_dir = '/Users/pvb/Dropbox/Oceanografia/Data/Satelite/noaa.oisst.v2.highres/NC'
elif os.uname().nodename.lower().find('rossby') != -1:
    data_dir = '/data/pvb/Satelite/noaa.oisst.v2.highres/NC'
    
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
