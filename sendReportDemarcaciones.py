from globales import *
from datetime import datetime
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from dotenv import load_dotenv

# ------------------------------------------------------------------------
# Inicio
# ------------------------------------------------------------------------
print('>>>>> sendReportDemarcaciones' )

## Read env data
load_dotenv()

SOURCE_IMAP = os.getenv("SOURCE_IMAP")
SOURCE_SMTP = os.getenv("SOURCE_SMTP")
ARGO_USER   = os.getenv("ARGO_USER")
ARGO_MAIL   = os.getenv("ARGO_MAIL")
ARGO_PASS   = os.getenv("ARGO_PASS")

analisisDir   = GlobalSU['AnaPath'] + '/SSTGlobalAnalysis/'
imagesDir     = GlobalSU['AnaPath'] + '/SSTGlobalAnalysis/images'

current_date = datetime.now().strftime('%d-%b-%Y %H:%M:%S')

msg = EmailMessage()
msg['Subject'] = 'Demarcaciones Analisis SST actualizado '+current_date
msg['From'] = formataddr(("IEOOS", ARGO_MAIL))
msg['To'] = 'pvelezbelchi@gmail.com'
msg.set_content('SST')

msg.add_alternative("""
<html>
  <body>
    <p><a href="https://www.oceanografia.es/IEOOS/SST/SST_NOR.html">NOR SST Analysis</a></p>
    <p><a href="https://www.oceanografia.es/IEOOS/SST/SST_SUD.html">SUD SST Analysis</a></p>
    <p><a href="https://www.oceanografia.es/IEOOS/SST/SST_CAN.html">CAN SST Analysis</a></p>
    <p><a href="https://www.oceanografia.es/IEOOS/SST/SST_ESA.html">ESA SST Analysis</a></p>
    <p><a href="https://www.oceanografia.es/IEOOS/SST/SST_LEB.html">LEB SST Analysis</a></p>

  </body>
</html>
""", subtype='html')

# Attach an image
with open(analisisDir+'/images/sstd_CAN.png', 'rb') as img:
    img_data = img.read()
    msg.add_attachment(img_data, maintype='image', subtype='png', filename='sstd_CAN.png')

with open(analisisDir+'/images/map_sstd_anom_CAN.png', 'rb') as img:
    img_data = img.read()
    msg.add_attachment(img_data, maintype='image', subtype='png', filename='map_sstd_anom_CAN.png')

# Send the email
with smtplib.SMTP_SSL(SOURCE_SMTP, 465) as smtp:
    smtp.login(ARGO_USER, ARGO_PASS)
    smtp.send_message(msg)

