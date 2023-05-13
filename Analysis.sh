#! /bin/zsh
source $HOME/.zshrc
source $HOME/.telegram

strval=$(uname -a)
if [[ $strval == *EemmMBP* ]];
then
  imagesDir=$HOME/Dropbox/Oceanografia/Analisis/SSTGlobalAnalysis/images
  pythonDir=/Users/pvb/miniconda3/envs/ocean/bin/python

fi
if [[ $strval == *rossby* ]];
then
  dataDir=$HOME/Analisis/SSTGlobalAnalysis/data
  imagesDir=$HOME/Analisis/SSTGlobalAnalysis/images
  pythonDir=/opt/conda/envs/ocean/bin/python
fi

#------------------------------------
#Inicio
#------------------------------------
printf ">>>> Updating SSTs \n"
printf "  imagesDir $imagesDir \n"
printf "  dataDir $dataDir \n"
printf "  pythonDir $pythonDir \n"

/bin/rm $dataDir/*.nc
/bin/rm $imagesDir/*.png

printf "   > Download data SSTs \n"
$pythonDir Analysis_DownloadData.py

printf "   > Update SSTs \n"
$pythonDir Analysis_data.py

printf "   > Plots SSTs \n"
$pythonDir Analysis_plots.py

printf "   > Plots Mapa anomalia \n"
$pythonDir Analysis_plots_maps.py


#------------------------------------
#TelegramBot
#------------------------------------

URL="https://api.telegram.org/bot$ArgoEsBotTOKEN/sendMessage"
URLimg="https://api.telegram.org/bot$ArgoEsBotTOKEN/sendphoto?chat_id=$ArgoEsChannel"
MENSAJE="Global Analisis SST"

curl -s -X POST $URL -d chat_id=$ArgoEsChannel -d text="$MENSAJE" -d parse_mode=html
#curl -F "photo=@$imagesDir/sstd_mean_GO.png" $URLimg -F caption="Global SST mean anomlay"
curl -F "photo=@$imagesDir/sstd_anom_mean_GO.png" $URLimg -F caption="Global SST mean anomlay"
curl -F "photo=@$imagesDir/sstd_GO.png" $URLimg -F caption="Global SST"
curl -F "photo=@$imagesDir//map_sstd_anom_GO.png" $URLimg -F caption="Map Anomalia SST"