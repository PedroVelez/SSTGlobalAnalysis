from globales import *
from datetime import datetime
import smtplib
from email.message import EmailMessage
from email.utils import formataddr

# ------------------------------------------------------------------------
# Inicio
# ------------------------------------------------------------------------
print('>>>>> sendReport' )

## Read env data
HOME=os.environ['HOME']
f = open(HOME+'/.env', 'r')
for line in f.readlines():
    Name=line.strip().split('=')[0]
    Content=line.strip().split('=')[-1]
    if Name=='EMAIL_ADDRESS' or Name=='EMAIL_PASSWORD' or Name=='USER_NAME':
        exec(Name + "=" + "'" + Content + "'")
f.close()


analisisDir   = GlobalSU['AnaPath'] + '/SSTGlobalAnalysis/'
imagesDir     = GlobalSU['AnaPath'] + '/SSTGlobalAnalysis/images'

current_date = datetime.now().strftime('%d-%b-%Y %H:%M:%S')

msg = EmailMessage()
msg['Subject'] = 'Global Analisis SST actualizado '+current_date
msg['From'] = formataddr(("IEOOS", EMAIL_ADDRESS))
msg['To'] = 'pvelezbelchi@gmail.com'
msg.set_content('Map Anomalia SST')

msg.add_alternative("""
<html>
  <body>
    <p><a href="https://www.oceanografia.es/pedro/research_SST_GLOBAL.html">Global SST Analysis</a></p>
    <p><a href="https://www.oceanografia.es/IEOOS/SST/SST_NOR.html">NOR SST Analysis</a></p>
    <p><a href="https://www.oceanografia.es/IEOOS/SST/SST_SUD.html">SUD SST Analysis</a></p>
    <p><a href="https://www.oceanografia.es/IEOOS/SST/SST_CAN.html">CAN SST Analysis</a></p>
    <p><a href="https://www.oceanografia.es/IEOOS/SST/SST_ESA.html">ESA SST Analysis</a></p>
    <p><a href="https://www.oceanografia.es/IEOOS/SST/SST_LEB.html">LEB SST Analysis</a></p>

  </body>
</html>
""", subtype='html')

# Attach an image
with open(analisisDir+'/images/map_sstd_anom_GO.png', 'rb') as img:
    img_data = img.read()
    msg.add_attachment(img_data, maintype='image', subtype='png', filename='map_sstd_anom_GO.png')

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

with open(analisisDir+'/images/sstd_NOR.png', 'rb') as img:
    img_data = img.read()
    msg.add_attachment(img_data, maintype='image', subtype='png', filename='sstd_NOR.png')
    
with open(analisisDir+'/images/sstd_SUD.png', 'rb') as img:
    img_data = img.read()
    msg.add_attachment(img_data, maintype='image', subtype='png', filename='sstd_SUD.png')

with open(analisisDir+'/images/sstd_CAN.png', 'rb') as img:
    img_data = img.read()
    msg.add_attachment(img_data, maintype='image', subtype='png', filename='sstd_CAN.png')

with open(analisisDir+'/images/sstd_ESA.png', 'rb') as img:
    img_data = img.read()
    msg.add_attachment(img_data, maintype='image', subtype='png', filename='sstd_ESA.png')

with open(analisisDir+'/images/sstd_LEB.png', 'rb') as img:
    img_data = img.read()
    msg.add_attachment(img_data, maintype='image', subtype='png', filename='sstd_LEB.png')


# Send the email
with smtplib.SMTP_SSL('smtpin.csic.es', 465) as smtp:
    smtp.login(USER_NAME, EMAIL_PASSWORD)
    smtp.send_message(msg)



