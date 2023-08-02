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

printf ">>>> Updating analisis global SSTs \n" > $analisisDir/updateSSTGlobal.log
printf ">>>> Updating analisis global SSTs \n"
printf "   > $strval\n" > $analisisDir/updateSSTGlobal.log
printf "   > $strval\n"

#------------------------------------
#Inicio
#------------------------------------
printf "   > Directorio $analisisDir \n"

/bin/rm $analisisDir/updateSSTGlobal.log
/bin/touch $analisisDir/updateSSTGlobal.log

printf "   > Download data from current year SSTs \n"
$pythonDir $analisisDir/downloadData.py

