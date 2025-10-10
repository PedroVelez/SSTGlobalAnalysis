from globales import *
from datetime import datetime
import smtplib
from email.message import EmailMessage
from email.utils import formataddr

# ------------------------------------------------------------------------
# Inicio
# ------------------------------------------------------------------------
print('>>>>> sendReportiDemarcacionesMUR' )

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
msg['Subject'] = 'Demarcaciones MUR Analisis SST actualizado '+current_date
msg['From'] = formataddr(("IEOOS", EMAIL_ADDRESS))
msg['To'] = 'pvelezbelchi@gmail.com'
msg.set_content('SST')

msg.add_alternative("""
<html>
  <body>
    <p><a href="https://www.oceanografia.es/IEOOS/SST/SSTMUR_NOR.html">NOR MUR SST Analysis</a></p>
    <p><a href="https://www.oceanografia.es/IEOOS/SST/SSTMUR_SUD.html">SUD MUR SST Analysis</a></p>
    <p><a href="https://www.oceanografia.es/IEOOS/SST/SSTMUR_CAN.html">CAN MUR SST Analysis</a></p>
    <p><a href="https://www.oceanografia.es/IEOOS/SST/SSTMUR_ESA.html">ESA MUR SST Analysis</a></p>
    <p><a href="https://www.oceanografia.es/IEOOS/SST/SSTMUR_LEB.html">LEB MUR SST Analysis</a></p>

  </body>
</html>
""", subtype='html')

# Attach an image
with open(analisisDir+'images/sstdMUR_CAN.png', 'rb') as img:
    img_data = img.read()
    msg.add_attachment(img_data, maintype='image', subtype='png', filename='sstdMUR_CAN.png')

with open(analisisDir+'images/map_sstdMUR_anom_CAN.png', 'rb') as img:
    img_data = img.read()
    msg.add_attachment(img_data, maintype='image', subtype='png', filename='map_sstdMUR_anom_CAN.png')



# Send the email
with smtplib.SMTP_SSL('smtpin.csic.es', 465) as smtp:
    smtp.login(USER_NAME, EMAIL_PASSWORD)
    smtp.send_message(msg)



