# Limpa a tela
clear

# Determina variavel de ambiente
export HOME_CM="/home/pi/caixa-magica"

# Mata processos pyconcrete
echo "-- FINALIZANDO PROCESSOS PYTHON3 --"
sudo pkill -9 -f pyconcrete

# Mata processos pyconcrete
echo "-- FINALIZANDO PROCESSOS PYCONCRETE --"
sudo pkill -9 -f pyconcrete

echo "Iniciando servico alive"
sudo pyconcrete /home/pi/caixa-magica/sincronismo/sincronismo_check_sistema_alive.pyee &

sleep 1

echo "-- REMOVENDO ANTIGO DIRETORIO TESTE HARDWARE --"
sudo rm -rf "/home/pi/caixa-magica-teste-HW"

# Executa script que reinicia o banco de dados, com as configuracoes necessarias
echo "Iniciando BD"
sudo pyconcrete /home/pi/caixa-magica/start_conf_postgresql.pyee

sudo pyconcrete /home/pi/caixa-magica/core/libera_portas.pyee

# Executa scripts de criação BD
sleep 2
echo "Rodando script criacao BD"
sudo pyconcrete /home/pi/caixa-magica/scripts_bd/script_bd.pyee

# Executa script criacao jsons basicos
cd $HOME_CM
sudo pyconcrete /home/pi/caixa-magica/gera_jsons_linha_base.pyee 
sudo pyconcrete /home/pi/caixa-magica/download_bibliotecas.pyee 

#FILE=$HOME_CM-teste-HW/teste_realizado.txt

#if test ! -f "$FILE"; then
#    sudo pyconcrete /home/pi/caixa-magica-teste-HW/view.pyee
#fi
unclutter -idle 0 &
xset s off &
xset -dpms &
xset s noblank &

echo "aqui 7"
echo "-- INICIANDO TELEMETRIA --"
sudo sh /home/pi/caixa-magica/start_telemetria.sh &

echo "-- INICIANDO APLICACAO --"
sudo pyconcrete /home/pi/caixa-magica/start.pyee

