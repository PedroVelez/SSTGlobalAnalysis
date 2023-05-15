#! /bin/zsh
source $HOME/.zshrc
source $HOME/.telegram

printf ">>>> Updating analisis global SSTs \n"

strval=$(uname -a)
printf "   > $strval\n"

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
printf "   > Directorio $analisisDir \n"

/bin/rm $analisisDir/Analysis.log
/bin/touch $analisisDir/Analysis.log

printf "   > Download data SSTs \n"
#$pythonDir Analysis_DownloadData.py >> $analisisDir/Analysis.log

printf "   > Update data SSTs \n"
/bin/rm $analisisDir/data/*.nc
$pythonDir Analysis_data.py >> $analisisDir/Analysis.log

printf "   > Plots SSTs \n"
#/bin/rm $analisisDir/images/*.png
#$pythonDir Analysis_plots.py >> $analisisDir/Analysis.log

printf "   > Plots Mapa anomalia \n"
#$pythonDir Analysis_plots_maps.py >> $analisisDir/Analysis.log

#------------------------------------
#TelegramBot
#------------------------------------

URL="https://api.telegram.org/bot$ArgoEsBotTOKEN/sendMessage"
URLimg="https://api.telegram.org/bot$ArgoEsBotTOKEN/sendphoto?chat_id=$ArgoEsChannel"
URLdoc="https://api.telegram.org/bot$ArgoEsBotTOKEN/sendDocument?chat_id=$ArgoEsChannel"

curl -s -X POST $URL -d chat_id=$ArgoEsChannel -d text="Global Analisis SST" -d parse_mode=html >> $analisisDir/Analysis.log
curl -F "photo=@$analisisDir/images/sstd_anom_mean_GO.png" $URLimg -F caption="Global SST mean anomlay" >> $analisisDir/Analysis.log
curl -F "photo=@$analisisDir/images/sstd_GO.png" $URLimg -F caption="Global SST" >> $analisisDir/Analysis.log
curl -F "photo=@$analisisDir/images/map_sstd_anom_GO.png" $URLimg -F caption="Map Anomalia SST" >> $analisisDir/Analysis.log
#curl -F "document=@$analisisDir/Analysis.log" $URLdoc >> $analisisDir/Analysis.log