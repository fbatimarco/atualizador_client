#!/bin/sh
echo "Obtendo versao do processador..."
versao_processador=$(eval "sudo python3 /home/pi/atualizador_client/pega_versao_proc.py")

echo "Versao obtida: "$versao_processador

sudo rm -rf /home/pi/atualizador_client/zip
sudo rm -rf /home/pi/atualizador_client/cminstaller*
sudo mkdir -p /home/pi/atualizador_client/zip
sudo rm -rf /home/pi/atualizador_client/zip/atualizador*
sudo rm -rf /home/pi/atualizador_client/zip/deploy_caixa-magica.zip

# Baixa o conteudo do repositorio
folder="cminstaller_"$versao_processador

echo "Baixando do repositorio (pode levar minutos)"
sudo rm -rf /home/pi/atualizador_client/$folder/
comando="sudo git clone https://github.com/fbatimarco/"$folder".git"
echo $comando
eval $comando
echo "Conteudo baixado do repositorio"
sleep 2

echo "Descompactando... (leva alguns segundos)"
sudo mv /home/pi/atualizador_client/$folder/caixa-magica-install.zip /home/pi/atualizador_client/zip/
sudo unzip /home/pi/atualizador_client/zip/caixa-magica-install.zip -d /home/pi/atualizador_client/zip/
sleep 2

echo "Descompactando..."
sudo unzip /home/pi/atualizador_client/zip/caixa-magica-install -d /home/pi/atualizador_client/zip/
sudo rm -rf /home/pi/atualizador_client/cminstaller*
sleep 2

echo "Executando atualizador..."
#sudo sh /home/pi/atualizador_client/zip/atualizador.sh
echo "Finalizado"
sleep 2

