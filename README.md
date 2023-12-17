O projeto implementa um Cliente, Servidor e uma aplicação utilizando sockets e threading no python.
Para evitar problemas de compatibilidade, utilizar o python 3.10
Passos para execução do projeto.
Para executar localmente, considerando dois dispositivos:
Inicialize o Servidor no ip 0.0.0.0:porta
Inicialize o Cliente ou aplicação configurando os parametros do cliente, apontando para o ip local da maquina a executar o servidor.
Aperte no botão para conectar.
Uma vez conectado, é possivel utilizar as funcionalidades da aplicação.

Caso o servidor esteja em uma rede diferente do Cliente, é necessario inicialmente liberar o acesso a porta no firewall dos dispositivos.
No roteador do Servidor, é necessario adicionar à tabela de encaminhamento do roteador, os dados da porta WAN, ip-local de destino, MAC, e porta de destino na maquina local.
Uma vez que o encaminhamento do portas e firewall estejam configurados, é possível rodar o servidor no ip 0.0.0.0:porta.
O cliente deve estar configurado para o ip externo da rede na qual a maquina está executando o Servidor, assim como a porta presente na tabela de encaminhamento.

É possível que mais de um client estabeleça conexão ao mesmo tempo com o servidor, pois o mesmo utiliza uma thread para cada socket conectado.

Funcionalidades:
1. Depositar. (Envia uma mensagem ao servidor para criar n_copias em n_caminhos diferentes, do arquivo exemplo.txt, que contém os dados dados_exemplo)
2. Recuperar. (Envia uma mensagem ao servidor para recuperar o arquivo exemplo.txt a partir de uma das copias presentes no Servidor)
3. Modificar quantidade de replicas (fator de replicação). (Envia uma mensagem ao servidor para modificar o número de cópias existentes no servidos. Pode ser utilizado para remover as copias utilizando 0 como parametro)
4. Desconectar. (Encerra a conexão do socket do client, liberando a thread no servidor)
