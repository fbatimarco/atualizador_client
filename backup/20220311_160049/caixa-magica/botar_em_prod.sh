echo 'Matando tudo'
sudo pkill -9 -f start_monitor.sh
killall -9 -f pyconcrete
killall -9 -f pyconcrete

echo 'Zerando pasta de fotos'
sudo rm -rf 	/home/pi/caixa-magica-img
sudo mkdir 	/home/pi/caixa-magica-img
echo 'Foi'

echo "Zerando logs"
sudo rm -rf /home/pi/caixa-magica-logs
sudo mkdir -p /home/pi/caixa-magica-logs

echo 'Zerando banco'
sh reset_bd.sh

echo 'Removendo os JSON de inicializacao e tal'
rm -f /home/pi/caixa-magica-operacao/inicializacao.json
rm -f /home/pi/caixa-magica-operacao/motorista.json
rm -f /home/pi/caixa-magica-operacao/viagem.json
rm -f /home/pi/caixa-magica-operacao/passagens_viagem.json
rm -f /home/pi/caixa-magica-operacao/instalacao.json
rm -f /home/pi/caixa-magica-operacao/aberto.txt
rm -f /home/pi/caixa-magica-operacao/idFechamentoViagem.json
echo 'Foi'

sudo touch /home/pi/caixa-magica-operacao/sincronismo.json
echo '{"url": "https://api-operacao.buspay.com.br/api/", "lastSyncAtualizacao": "2020-10-23T17:00:23.722199", "lastSyncBloq": "2020-10-27T22:55:43.267869", "lastSyncDesbloq": "2020-10-27T22:55:42.659562"}' > /home/pi/caixa-magica-operacao/sincronismo.json
echo 'Reset efetuado'

sudo pkill -9 -f pyconcrete
sudo pkill -9 -f pyconcrete
