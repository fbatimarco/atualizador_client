#!/bin/bash

filename='check_start_sh.txt'
string_to_find='sh /home/pi/caixa-magica/start.sh'

while :
do
  # grava localmente um arquivo checando o status do start.sh
  ps -ef | grep start.sh | tee $filename

  n=1
  jaemexec=false
  
  while read line; do
    echo "Linha: $line"

    if [[ $line == *"$string_to_find"* ]]; then
        jaemexec=true
    	break
    fi

    n=$((n+1))    
  done < $filename

    if [[ $jaemexec == false ]]; then
        lxterminal -e "sudo sh /home/pi/caixa-magica/start.sh"
    fi

  sleep 1
done
