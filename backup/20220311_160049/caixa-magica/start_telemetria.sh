echo "-- INICIANDO TELEMETRIA --"
sudo rm -f /home/pi/telemetria.pye 
sudo pyconcrete telemetria.pye &
echo "-- TELEMETRIA INICIALIZADA --"

#sudo echo "import os" | tee -a /home/pi/telemetria.pye
#sudo echo "os.system('sudo pyconcrete telemetria.pye')" | tee -a /home/pi/telemetria.pye
