echo "-- INICIANDO TELEMETRIA --"
sudo rm -f /home/pi/telemetria.pyee 
sudo pyconcrete telemetria.pyee &
echo "-- TELEMETRIA INICIALIZADA --"

#sudo echo "import os" | tee -a /home/pi/telemetria.pyee
#sudo echo "os.system('sudo pyconcrete telemetria.pyee')" | tee -a /home/pi/telemetria.pyee
