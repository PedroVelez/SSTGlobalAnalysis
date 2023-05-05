#! /bin/zsh
source $HOME/.zshrc
source $HOME/.telegram

conda activate ocean
/Users/pvb/miniconda3/envs/ocean/bin/python SSTAnalysis_daily_Plots.py


URL="https://api.telegram.org/bot$ArgoEsBotTOKEN/sendMessage"
URLimg="https://api.telegram.org/bot$ArgoEsBotTOKEN/sendphoto?chat_id=$ArgoEsChannel"
MENSAJE="Global Analisis SST"

curl -s -X POST $URL -d chat_id=$ArgoEsChannel -d text="$MENSAJE" -d parse_mode=html
curl -F "photo=@$HOME/Analisis/SSTGlobalAnalysis/images/sstd_GO_mean.png" $URLimg -F caption="Global SST mean anomlay"
curl -F "photo=@$HOME/Analisis/SSTGlobalAnalysis/images/sstd_anom_GO_mean.png" $URLimg -F caption="Global SST mean anomlay"
curl -F "photo=@$HOME/Analisis/SSTGlobalAnalysis/images/sstd_GO.png" $URLimg -F caption="Global SST mean anomlay"
curl -F "photo=@$HOME/Analisis/SSTGlobalAnalysis/images/sstd_anom_GO.png" $URLimg -F caption="Global SST mean anomlay"

