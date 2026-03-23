import ftplib
import datetime
import os
import glob
from dotenv import load_dotenv
from globales import *


# ------------------------------------------------------------------------
# Inicio
# ------------------------------------------------------------------------
print('>>>>> uploadImages' )

## Read env data
load_dotenv()
userFTP = os.getenv("userFTP")
passwdFTP = os.getenv("passwdFTP")

imagesDir = GlobalSU['ProPath'] + '/SSTGlobalAnalysis/images'
os.chdir(imagesDir)

## Global analisis
session = ftplib.FTP('ftp.oceanografia.es',userFTP,passwdFTP)
session.cwd('/html/pedro/images/SST')
Titulos_short = ['GO','NH','SH','NAtl']

# Read and upload files
for it in range(0,len(Titulos_short)):
    titulo_short = Titulos_short[it]
    filenames = glob.glob(imagesDir+'/*'+titulo_short+'*.png')
    for filename in filenames:
        print('    > https://www.oceanografia.es/pedro/images/SST/'+filename.split('/')[-1])
        session.storbinary('STOR '+ filename.split('/')[-1], open(filename, 'rb'))
session.quit()


print('      uploadImages <<<<<' )