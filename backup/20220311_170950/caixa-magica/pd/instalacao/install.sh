if [ ! -e "/home/pi/caixa-magica" ]
then
    sudo mkdir -p "/home/pi/caixa-magica"
    sudo mkdir -p "/home/pi/caixa-magica/dig"
    sudo cp -R "caixa-magica.zip" "/home/pi/caixa-magica"
fi

cd "/home/pi/caixa-magica"

sudo unzip "caixa-magica.zip"

sudo rm -fR "caixa-magica.zip"

sudo chmod -R 777 "/home/pi/caixa-magica"

sudo cp /home/pi/caixa-magica/*.so /lib/

#Cria os links
sudo ln -s -f "/home/pi/caixa-magica/run_caixa_magica.sh" "/home/pi/Desktop"
sudo ln -s -f "/home/pi/caixa-magica/run_gravador.sh" "/home/pi/Desktop"

echo "Para executar o gravador de digitais: cd /home/pi/caixa-magica/ && ./run_gravador.sh"
echo "Para executar a Caixa Mágica:         cd /home/pi/caixa-magica/ && ./run_caixa_magica.sh"
