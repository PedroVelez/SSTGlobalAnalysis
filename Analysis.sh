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

printf ">>>> Updating analisis global SSTs \n" > $analisisDir/Analysis.log
printf ">>>> Updating analisis global SSTs \n"
printf "   > $strval\n" > $analisisDir/Analysis.log
printf "   > $strval\n"

#------------------------------------
#Inicio
#------------------------------------
printf "   > Directorio $analisisDir \n"

/bin/rm $analisisDir/Analysis.log
/bin/touch $analisisDir/Analysis.log

printf "   > Download data from current year SSTs \n"
$pythonDir $analisisDir/Analysis_DownloadData.py >> $analisisDir/Analysis.log

printf "   > Update data SSTs \n"
/bin/rm $analisisDir/data/*.nc
$pythonDir $analisisDir/Analysis_data.py >> $analisisDir/Analysis.log

printf "   > Plots SSTs \n"
#/bin/rm $analisisDir/images/*.png
$pythonDir $analisisDir/Analysis_plots.py >> $analisisDir/Analysis.log

printf "   > Plots Mapa anomalia \n"
$pythonDir Analysis_plots_maps.py >> $analisisDir/Analysis.log

printf "   > Upload Plots \n"
$pythonDir Analysis_UploadImages.py >> $analisisDir/Analysis.log


#------------------------------------
#TelegramBot
#------------------------------------

URL="https://api.telegram.org/bot$ArgoEsBotTOKEN/sendMessage"
URLimg="https://api.telegram.org/bot$ArgoEsBotTOKEN/sendphoto?chat_id=$ArgoEsChannel"
URLdoc="https://api.telegram.org/bot$ArgoEsBotTOKEN/sendDocument?chat_id=$ArgoEsChannel"

curl -s -X POST $URL -d chat_id=$ArgoEsChannel -d text="Global Analisis SST" -d parse_mode=html
curl -F "photo=@$analisisDir/images/sstd_anom_mean_GO.png" $URLimg -F caption="Global SST mean anomlay"
curl -F "photo=@$analisisDir/images/sstd_GO.png" $URLimg -F caption="Global SST"
curl -F "photo=@$analisisDir/images/map_sstd_anom_GO.png" $URLimg -F caption="Map Anomalia SST"
curl -s -X POST $URL -d chat_id=$ArgoEsChannel -d text="<strong>Log</strong>%0A%0A `date +"%b %d %T"` %0A`cat /home/pvb/Analisis/SSTGlobalAnalysis/Analysis.log` %0A" -d parse_mode=html

