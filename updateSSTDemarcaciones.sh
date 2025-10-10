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

/bin/rm $analisisDir/updateSSTDemarcaciones.log
/bin/touch $analisisDir/updateSSTDemarcaciones.log

printf ">>>> Updating analisis Demarcaciones SSTs \n"
printf "   > $strval\n"
start=$SECONDS

#------------------------------------
#Inicio
#------------------------------------
printf "   > Directorio $analisisDir \n"

#printf "   > Download data from current year SSTs \n"
#$pythonDir $analisisDir/downloadData.py

printf "   > Update data SSTs demarcaciones\n"
/bin/rm $analisisDir/data/sstd_*CAN.nc
/bin/rm $analisisDir/data/sstd_*ESA.nc
/bin/rm $analisisDir/data/sstd_*IBICan.nc
/bin/rm $analisisDir/data/sstd_*LEB.nc
/bin/rm $analisisDir/data/sstd_*NOR.nc
/bin/rm $analisisDir/data/sstd_*IBICan.nc
/bin/rm $analisisDir/data/sstLD_*CAN.nc
/bin/rm $analisisDir/data/sstLD_*ESA.nc
/bin/rm $analisisDir/data/sstLD_*IBICan.nc
/bin/rm $analisisDir/data/sstLD_*LEB.nc
/bin/rm $analisisDir/data/sstLD_*NOR.nc
/bin/rm $analisisDir/data/sstLD_*IBICan.nc
$pythonDir $analisisDir/analysisDataDemarcaciones.py

elapsed=$SECONDS
duration=$(( elapsed - start ))
printf "   > $elpased seconds \n"


printf "   > Plots SSTs \n"
/bin/rm $analisisDir/images/*CAN*.png
/bin/rm $analisisDir/images/*ESA*.png
/bin/rm $analisisDir/images/*IBICan*.png
/bin/rm $analisisDir/images/*LEB*.png
/bin/rm $analisisDir/images/*NOR*.png
/bin/rm $analisisDir/images/*IBICan*.png
$pythonDir $analisisDir/plotsTimeSeriesDemarcaciones.py

printf "   > Plots Mapa anomalia \n"
$pythonDir $analisisDir/plotsMapAnomaliasDemarcaciones.py 

printf "   > Upload Plots \n"
$pythonDir $analisisDir/uploadImages.py

printf "   > Send Report \n"
$pythonDir $analisisDir/sendReportDemarcaciones.py



end=$SECONDS
duration=$(( end - start ))
printf "   > $duration seconds to complete\n"
