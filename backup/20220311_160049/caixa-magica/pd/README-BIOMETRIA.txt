Funcionamento da Biometria em Linux Ubuntu 32 bits

Para executar a aplicação em Linux é necessário realizar os seguintes passos:

- Dar permissão completo a pasta lib do sistema 
- Vá até a pasta raiz do sistema e excute o comando sudo chmod 777 /lib

- Em seguida, vá até o diretório do projeto \lib\so\x86 e copie os arquivos para dentro da pasta lib
que você acabou de dar as permissões.

Após isso, apenas executar o projeto o arquivo "GravadorBiometrico.pye" com o leitor Plugado na porta USB para executar a gravação das 
biometrias.

O arquivo Application.pye é a aplicação da caixa mágica.
O arquivo GravadorBiometrico.pye é o arquivo que executa um software a parte para gravação das biometrias