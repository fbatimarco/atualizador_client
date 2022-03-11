sudo mkdir -p /home/pi/atualizador_client/zip
sudo rm -rf /home/pi/atualizador_client/zip/atualizador*
sudo rm -rf /home/pi/atualizador_client/zip/deploy_caixa-magica.zip

echo "Descompactando..."
sudo unzip /home/pi/atualizador_client/zip/caixa-magica-install -d /home/pi/atualizador_client/zip/
sleep 2

echo "Executando atualizador..."
sudo sh /home/pi/atualizador_client/zip/atualizador.sh
echo "Finalizado"
sleep 2



