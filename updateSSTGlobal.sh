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
/bin/rm $analisisDir/data/sstd_*GO.nc
/bin/rm $analisisDir/data/sstd_*NH.nc
/bin/rm $analisisDir/data/sstd_*SH.nc
/bin/rm $analisisDir/data/sstd_*NAtl.nc
/bin/rm $analisisDir/data/sstLD_*GO.nc
/bin/rm $analisisDir/data/sstLD_*NH.nc
/bin/rm $analisisDir/data/sstLD_*SH.nc
/bin/rm $analisisDir/data/sstLD_*NAtl.nc
$pythonDir $analisisDir/analysisData.py

elapsed=$SECONDS
duration=$(( elapsed - start ))
printf "   > $elpased seconds \n"

printf "   > Plots SSTs \n"
#/bin/rm $analisisDir/images/*.png
/bin/rm $analisisDir/images/*GO*.png
/bin/rm $analisisDir/images/*NH*.png
/bin/rm $analisisDir/images/*SH*.png
/bin/rm $analisisDir/images/*NAtl*.png

$pythonDir $analisisDir/plotsTimeSeries.py

printf "   > Plots Mapa anomalia \n"
$pythonDir $analisisDir/plotsMapAnomalias.py 

printf "   > Plots comparacionHS \n"
$pythonDir $analisisDir/plotsComparaHemispheres.py 

printf "   > Upload Plots \n"
$pythonDir $analisisDir/uploadImages.py

printf "   > Send Report \n"
$pythonDir $analisisDir/sendReportGlobal.py


end=$SECONDS
duration=$(( end - start ))
printf "   > $duration seconds to complete\n"
