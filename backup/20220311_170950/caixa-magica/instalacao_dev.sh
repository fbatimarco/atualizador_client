sudo rm -rf /home/pi/caixa-magica-operacao/sincronismo.json

sudo touch /home/pi/caixa-magica-operacao/sincronismo.json
echo '{"url": "https://api-operacao.dev.buspay.com.br/api/", "lastSyncAtualizacao": "2020-10-23T17:00:23.722199", "lastSyncBloq": "2020-10-27T22:55:43.267869", "lastSyncDesbloq": "2020-10-27T22:55:42.659562"}' > /home/pi/caixa-magica-operacao/sincronismo.json
