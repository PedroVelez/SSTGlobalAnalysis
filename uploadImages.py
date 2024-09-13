import ftplib
import datetime
import os
import glob

## Read env data
HOME=os.environ['HOME']   
f = open(HOME+'/.env', 'r')
for line in f.readlines():
    Name=line.strip().split('=')[0]
    Content=line.strip().split('=')[-1]
    if Name=='dirData' or Name=='dirAnalisis' or Name=='userFTP' or Name=='passwdFTP':
        exec(Name + "=" + "'" + Content + "'")
f.close()

if os.uname().nodename.lower().find('eemmmbp') != -1:
    imagesDir = dirAnalisis + '/SSTGlobalAnalysis/images'
elif os.uname().nodename.lower().find('rossby') != -1:
    imagesDir = dirAnalisis + '/SSTGlobalAnalysis/images'

os.chdir(imagesDir)
session = ftplib.FTP('ftp.oceanografia.es',userFTP,passwdFTP)
session.cwd('/html/pedro/images/SST')

#Read and uplod files
filenames = glob.glob(imagesDir+'/*.png')

for filename in filenames:
    print('https://www.oceanografia.es/pedro/images/SST/'+filename.split('/')[-1])
    session.storbinary('STOR '+ filename.split('/')[-1], open(filename, 'rb'))

session.quit()    
