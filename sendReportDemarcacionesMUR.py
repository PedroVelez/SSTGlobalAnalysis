from globales import *
from datetime import datetime
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from dotenv import load_dotenv

# ------------------------------------------------------------------------
# Inicio
# ------------------------------------------------------------------------
print('>>>>> sendReportDemarcacionesMUR' )

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
msg['Subject'] = 'Demarcaciones MUR Analisis SST actualizado '+current_date
msg['From'] = formataddr(("IEOOS", ARGO_MAIL))
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
with smtplib.SMTP_SSL(SOURCE_SMTP, 465) as smtp:
    smtp.login(ARGO_USER, ARGO_PASS)
    smtp.send_message(msg)


