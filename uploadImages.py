import ftplib
import datetime
import os
import glob
from globales import *
# ------------------------------------------------------------------------
# Inicio
# ------------------------------------------------------------------------

## Read env data
HOME=os.environ['HOME']   
f = open(HOME+'/.env', 'r')
for line in f.readlines():
    Name=line.strip().split('=')[0]
    Content=line.strip().split('=')[-1]
    if Name=='dirData' or Name=='dirAnalisis' or Name=='userFTP' or Name=='passwdFTP':
        exec(Name + "=" + "'" + Content + "'")
f.close()

imagesDir = GlobalSU['AnaPath'] + '/SSTGlobalAnalysis/images'

os.chdir(imagesDir)

## Global analisis
session = ftplib.FTP('ftp.oceanografia.es',userFTP,passwdFTP)
session.cwd('/html/pedro/images/SST')
Titulos_short = ['GO','NH','SH','NAtl']

#Read and uplod files
for it in range(0,len(Titulos_short)):
    titulo_short = Titulos_short[it]
    filenames = glob.glob(imagesDir+'/*'+titulo_short+'*.png')
    for filename in filenames:
        print('https://www.oceanografia.es/pedro/images/SST/'+filename.split('/')[-1])
        session.storbinary('STOR '+ filename.split('/')[-1], open(filename, 'rb'))
session.quit()

## Demarcaciones
session = ftplib.FTP('ftp.oceanografia.es',userFTP,passwdFTP)
session.cwd('/html/IEOOS/SST/images')
Titulos_short = ['LEB', 'NOR','CAN','SUD','ESA','IBICan']
#Read and uplod files
for it in range(0,len(Titulos_short)):
    titulo_short = Titulos_short[it]
    filenames = glob.glob(imagesDir+'/*'+titulo_short+'*.png')
    for filename in filenames:
        print('https://www.oceanografia.es/IEOOS/SST/images/'+filename.split('/')[-1])
        session.storbinary('STOR '+ filename.split('/')[-1], open(filename, 'rb'))

session.quit()    
