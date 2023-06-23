import ftplib
import datetime
import os
import glob

if os.uname().nodename.lower().find('eemmmbp') != -1:
    imagesDir = '/home/pvb/Dropbox/Oceanografia/Analisis/SSTGlobalAnalysis/images'
elif os.uname().nodename.lower().find('rossby') != -1:
    imagesDir = '/home/pvb/Analisis/SSTGlobalAnalysis/images'

HOME=os.environ['HOME']   

## read user 
f = open(HOME+'/.env', 'r')
for line in f.readlines():
    Name=line.strip().split('=')[0]
    Content=line.strip().split('=')[-1]
    if Name=='userFTP' or Name=='passwdFTP':
        exec(Name + "=" + "'" + Content + "'")
f.close()

os.chdir(imagesDir)
session = ftplib.FTP('ftp.oceanografia.es',userFTP,passwdFTP)
session.cwd('/html/pedro/images/SST')

#Read and uplod files
filenames = glob.glob(imagesDir+'/*.png')

for filename in filenames:
    print('https://www.oceanografia.es/pedro/images/SST/'+filename.split('/')[-1])
    session.storbinary('STOR '+ filename.split('/')[-1], open(filename, 'rb'))

session.quit()    