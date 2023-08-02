#! /bin/zsh
source $HOME/.zshrc
source $HOME/.env

## SEtting bases on computer
strval=$(uname -a)
if [[ $strval == *EemmMBP* ]];
then
  analisisDir=$HOME/Dropbox/Oceanografia/Analisis/SSTGlobalAnalysis
  pythonDir=/Users/pvb/miniconda3/envs/ocean/bin/python
fi
if [[ $strval == *rossby* ]];
then
  analisisDir=$HOME/Analisis/SSTGlobalAnalysis
  pythonDir=/opt/conda/envs/ocean/bin/python
fi

#------------------------------------
#Inicio
#------------------------------------
/bin/rm $analisisDir/images/*.png

printf "   > Plots SSTs \n"
$pythonDir $analisisDir/plotsTimeSeries.py

printf "   > Plots Mapa anomalia \n"
$pythonDir $analisisDir/plotsMapAnomalies.py

printf "   > Plots comparacionHS \n"
$pythonDir $analisisDir/plotsComparaHemispheres.py

printf "   > Upload Plots \n"
$pythonDir $analisisDir/uploadImages.py 


#------------------------------------
#TelegramBot
#------------------------------------

URL="https://api.telegram.org/bot$ArgoEsBotTOKEN/sendMessage"
URLimg="https://api.telegram.org/bot$ArgoEsBotTOKEN/sendphoto?chat_id=$ArgoEsChannel"
URLdoc="https://api.telegram.org/bot$ArgoEsBotTOKEN/sendDocument?chat_id=$ArgoEsChannel"

curl -s -X POST $URL -d chat_id=$ArgoEsChannel -d text="Global Analisis SST" -d parse_mode=html
curl -F "photo=@$analisisDir/images/map_sstd_anom_GO.png" $URLimg -F caption="Map Anomalia SST"
curl -F "photo=@$analisisDir/images/sstd_GO.png" $URLimg -F caption="Global SST"
curl -F "photo=@$analisisDir/images/sstd_anom_mean_GO_HN_HS.png" $URLimg -F caption="Compare HGlobal SST"
curl -F "photo=@$analisisDir/images/sstd_anom_mean_NAtl.png" $URLimg -F caption="Atlantico Norte promedio SST"
curl -F "photo=@$analisisDir/images/sstd_anom_NAtl.png" $URLimg -F caption="Atlantico Norte SST"

