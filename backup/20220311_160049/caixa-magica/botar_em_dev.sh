echo 'Matando tudo'
killall -9 pyconcrete

echo 'Zerando pasta de fotos'
rm -rf 	/home/pi/caixa-magica-img
mkdir 	/home/pi/caixa-magica-img
echo 'Foi'

echo 'Zerando banco'
pyconcrete /home/pi/caixa-magica/delete_database_info.pye
echo 'Foi'

echo 'Removendo os JSON de inicializacao e tal'
rm -f /home/pi/caixa-magica-operacao/inicializacao.json
rm -f /home/pi/caixa-magica-operacao/motorista.json
rm -f /home/pi/caixa-magica-operacao/viagem.json
rm -f /home/pi/caixa-magica-operacao/passagens_viagem.json
rm -f /home/pi/caixa-magica-operacao/instalacao.json
rm -f /home/pi/caixa-magica-operacao/aberto.txt
rm -f /home/pi/caixa-magica-operacao/idFechamentoViagem.json
echo 'Foi'

echo 'Tá em DEV??'
sudo touch /home/pi/caixa-magica-operacao/sincronismo.json
echo '{"url": "https://api-operacao.dev.buspay.com.br/api/", "lastSyncAtualizacao": "2020-10-23T17:00:23.722199", "lastSyncBloq": "2020-10-27T22:55:43.267869", "lastSyncDesbloq": "2020-10-27T22:55:42.659562"}' > /home/pi/caixa-magica-operacao/sincronismo.json
echo 'Agora tá'
sudo reboot -f
