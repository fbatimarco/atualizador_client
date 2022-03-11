# Determina variavel de ambiente
export HOME_CM="/home/pi/caixa-magica"

echo "-- RECRIANDO BANCO DE DADOS --"
# Executa scripts de criação BD
cd $HOME_CM/scripts_bd
sudo pyconcrete script_bd.pye drop

sudo pkill -9 -f python
sudo pkill -9 -f pyconcrete
