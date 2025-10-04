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

/bin/rm $analisisDir/updateSSTMUR.log
/bin/touch $analisisDir/updateSSTMUR.log

printf ">>>> Updating analisis global SSTs \n"
printf "   > $strval\n"
start=$SECONDS

#------------------------------------
#Inicio
#------------------------------------
printf "   > Directorio $analisisDir \n"

printf "   > Update data SSTs MUR demarcaciones\n"
/bin/rm $analisisDir/data/sstdMUR_*CAN.nc
/bin/rm $analisisDir/data/sstdMUR_*ESA.nc
/bin/rm $analisisDir/data/sstdMUR_*IBICan.nc
/bin/rm $analisisDir/data/sstdMUR_*LEB.nc
/bin/rm $analisisDir/data/sstdMUR_*NOR.nc
/bin/rm $analisisDir/data/sstdMUR_*IBICan.nc
/bin/rm $analisisDir/data/sstLDMUR_*CAN.nc
/bin/rm $analisisDir/data/sstLDMUR_*ESA.nc
/bin/rm $analisisDir/data/sstLDMUR_*IBICan.nc
/bin/rm $analisisDir/data/sstLDMUR_*LEB.nc
/bin/rm $analisisDir/data/sstLDMUR_*NOR.nc
/bin/rm $analisisDir/data/sstLDMUR_*IBICan.nc

$pythonDir $analisisDir/analysisDataDemarcacionesMUR.py

elapsed=$SECONDS
duration=$(( elapsed - start ))
printf "   > $elpased seconds \n"


printf "   > Plots SSTs MUR \n"
/bin/rm $analisisDir/images/*MUR*.png
$pythonDir $analisisDir/plotsTimeSeriesDemarcacionesMUR.py

printf "   > Plots Mapa anomalia MUR \n"
$pythonDir $analisisDir/plotsMapAnomaliesDemarcacionesMUR.py 

printf "   > Upload Plots \n"
$pythonDir $analisisDir/uploadImages.py

end=$SECONDS
duration=$(( end - start ))
printf "   > $duration seconds to complete\n"
