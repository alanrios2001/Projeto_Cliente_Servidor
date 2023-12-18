import socket
import threading
from pathlib import Path


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))

    def listen(self):
        # espera por conexoes de clients
        self.sock.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client, address = self.sock.accept()
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client_socket):
        # recebe comandos do client
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            command, *args = data.split(' ')
            if command == 'DEPOSIT':
                self.handle_deposit(client_socket, *args)
            elif command == 'RECOVER':
                self.handle_recover(client_socket, *args)
            elif command == 'UPDATE':
                self.handle_update(client_socket, *args)
            else:
                client_socket.send(b'Comando invalido')
        client_socket.close()

    def handle_deposit(self, client_socket, filename, replication_factor):
        # recebe conteudo do arquivo
        file_content = client_socket.recv(1024).decode('utf-8')

        #cria pasta a ser armazenada
        path = f'copias/{filename}'
        Path(path).mkdir(parents=True, exist_ok=True)
        #verifica se já existem copias do arquivo
        copias = [f.name for f in Path(path).iterdir() if f.is_dir()]
        #se existirem, apaga as copias
        if copias:
            for copia in copias:
                for f in Path(f'{path}/{copia}').iterdir():
                    if f.is_file():
                        f.unlink()
        #armazena com numero de replicas especificado
        for i in range(int(replication_factor)):
            Path(f'{path}/copia_{i}_').mkdir(parents=True, exist_ok=True)
            with open(f'{path}/copia_{i}_/data.txt', 'a') as file:
                file.write(file_content)
        client_socket.send(b'Arquivo armazenado com sucesso')

    def handle_recover(self, client_socket, filename):
        #recupera os nome de pastas na pasta copias
        path = f'copias/'
        copias = [f.name for f in Path(path).iterdir() if f.is_dir()]
        if filename in copias:
            copy_paths = [f.name for f in Path(f'{path}/{filename}').iterdir() if f.is_dir()]
            with open(f'{path}/{filename}/{copy_paths[0]}/data.txt', 'r') as file:
                file_content = file.read()
            client_socket.send(file_content.encode('utf-8'))
        else:
            client_socket.send(b'Aquivo nao encontrado')

    def handle_update(self, client_socket, filename, new_replication_factor):
        #recupera os nome de pastas na pasta copias
        path = f'copias/'
        file_names = [f.name for f in Path(path).iterdir() if f.is_dir()]
        if filename in file_names:
            #recupera a quantidade de arquivos dentro da pasta copias/filename
            copias = [f.name for f in Path(f'{path}/{filename}').iterdir() if f.is_dir()]
            q_copias = len(copias)
            #se a quantidade de copias for menor que a nova quantidade de replicas, cria novas copias
            if int(new_replication_factor) == 0:
                for copia in copias:
                    for f in Path(f'{path}/{filename}/{copia}').iterdir():
                        if f.is_file():
                            f.unlink()
                    Path(f'{path}/{filename}/{copia}').rmdir()
                Path(f'{path}/{filename}').rmdir()

            elif q_copias < int(new_replication_factor):
                with open(f'{path}/{filename}/{copias[0]}/data.txt', 'r') as f:
                    file_content = f.read()
                last_id = int(copias[-1].split('_')[1]) + 1
                for i in range(int(new_replication_factor) - q_copias):
                    Path(f'{path}/{filename}/copia_{last_id}_').mkdir(parents=True, exist_ok=True)
                    with open(f'{path}/{filename}/copia_{last_id}_/data.txt', 'a') as file:
                        file.write(file_content)
                    last_id += 1
            #se a quantidade de copias for maior que a nova quantidade de replicas, apaga copias
            elif q_copias > int(new_replication_factor):
                for i in range(q_copias - int(new_replication_factor)):
                    last_id = int(copias[-1].split('_')[1])
                    for f in Path(f'{path}/{filename}/copia_{last_id}_').iterdir():
                        if f.is_file():
                            f.unlink()
                    Path(f'{path}/{filename}/copia_{last_id}_').rmdir()
                    copias = [f.name for f in Path(f'{path}/{filename}').iterdir() if f.is_dir()]
            client_socket.send(b'Fator de replicacao atualizado com sucesso')
        else:
            client_socket.send(b'Aquivo nao encontrado')


if __name__ == '__main__':
    server = Server('localhost', 12345)
    threading.Thread(target=server.listen).start()
