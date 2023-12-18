import socket
import time

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.host, self.port))

    def deposit(self, filename, q_replicas):
        # le conteudo do arquivo
        with open(filename, 'r') as file:
            file_content = file.read()
        # envia comando e argumentos para o servidor
        self.sock.send(f'DEPOSIT {filename} {q_replicas}'.encode('utf-8'))
        time.sleep(0.1)
        self.sock.send(file_content.encode('utf-8'))
        print(self.sock.recv(1024).decode('utf-8'))

    def recover(self, filename):
        # envia comando e argumentos para o servidor
        self.sock.send(f'RECOVER {filename}'.encode('utf-8'))
        file_content = self.sock.recv(1024).decode('utf-8')
        if file_content:
            if file_content != "Aquivo nao encontrado":
                # salva arquivo recuperado
                with open(f'recovered_{filename}', 'w') as file:
                    file.write(file_content)
                print('File recovered successfully')
            else:
                print('File not found')

    def update_replication(self, filename, nova_q_replicas):
        # envia comando e argumentos para o servidor
        self.sock.send(f'UPDATE {filename} {nova_q_replicas}'.encode('utf-8'))
        print(self.sock.recv(1024).decode('utf-8'))

    def close(self):
        self.sock.close()

    def run(self):
        self.connect()
        while True:
            print("Menu:\n1 - Deposit\n2 - Recover\n3 - Update\n4 - Exit")
            option = input("Choose an option: ")
            if option == '1':
                filename = input("Filename: ")
                q_replicas = input("Replication factor: ")
                self.deposit(filename, q_replicas)
            elif option == '2':
                filename = input("Filename: ")
                self.recover(filename)
            elif option == '3':
                filename = input("Filename: ")
                nova_q_replicas = input("New replication factor: ")
                self.update_replication(filename, nova_q_replicas)
            elif option == '4':
                self.close()
                break
            else:
                print("Invalid option")



if __name__ == '__main__':
    # cria um client e conecta ao servidor
    try:
        client = Client('ip_servidor_aqui', 50000)
        client.connect()
    except Exception as e:
        print(e)
        exit()
    file_name = 'testfile.txt'

    # envia arquivo
    client.deposit(file_name, 3)

    # recupera arquivo
    client.recover(file_name)

    # atualiza o fator de replicação
    #client.update_replication(file_name, 2)

    # fecha conexao com o servidor
    client.close()
