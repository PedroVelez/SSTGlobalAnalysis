#! /bin/zsh
source $HOME/.zshrc
source $HOME/.env

# Settings based on computer
strval=$(uname -a)
if [[ $strval == *EemmMBP* ]];
then
  analisisDir=$HOME/Dropbox/Oceanografia/Analisis/SSTGlobalAnalysis
  pythonDir=$HOME/miniconda3/envs/ocean/bin/python
fi
if [[ $strval == *rossby* ]];
then
  analisisDir=$HOME/Analisis/SSTGlobalAnalysis
  pythonDir=/opt/conda/envs/ocean/bin/python
fi

/bin/rm $analisisDir/updateSSTGlobal.log
/bin/touch $analisisDir/updateSSTGlobal.log

printf ">>>> Updating analisis global SSTs \n"
printf "   > $strval\n"
start=$SECONDS

#------------------------------------
#Inicio
#------------------------------------
printf "   > Directorio $analisisDir \n"

printf "   > Download data from current year SSTs \n"
$pythonDir $analisisDir/downloadData.py

printf "   > Update data SSTs \n"
/bin/rm $analisisDir/data/sst*GO*.nc
/bin/rm $analisisDir/data/sst*NH*.nc
/bin/rm $analisisDir/data/sst*SH*.nc
/bin/rm $analisisDir/data/sst*NAtl*.nc
$pythonDir $analisisDir/analysisData.py

elapsed=$SECONDS
duration=$(( elapsed - start ))
printf "   > $elpased seconds \n"


printf "   > Update data SSTs demarcaciones\n"
/bin/rm $analisisDir/data/sst*CAN*.nc
/bin/rm $analisisDir/data/sst*LEB*.nc
/bin/rm $analisisDir/data/sst*NOR*.nc
/bin/rm $analisisDir/data/sst*IBICan*.nc
$pythonDir $analisisDir/analysisDataDemarcaciones.py

elapsed=$SECONDS
duration=$(( elapsed - start ))
printf "   > $elpased seconds \n"


printf "   > Plots SSTs \n"
/bin/rm $analisisDir/images/*.png
$pythonDir $analisisDir/plotsTimeSeries.py
$pythonDir $analisisDir/plotsTimeSeriesDemarcaciones.py

printf "   > Plots Mapa anomalia \n"
$pythonDir $analisisDir/plotsMapAnomalies.py 
$pythonDir $analisisDir/plotsMapAnomaliesDemarcaciones.py 

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

end=$SECONDS
duration=$(( end - start ))
printf "   > $duration seconds to complete\n"
