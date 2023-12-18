import tkinter as tk
from tkinter import filedialog, simpledialog
from client import Client


class ConnectionScreen:
    def __init__(self, root, on_connect_callback):
        self.root = root
        self.on_connect_callback = on_connect_callback

        self.frame = tk.Frame(root)
        self.label = tk.Label(self.frame, text="Bem vindo ao APP")
        self.label.pack(pady=10)

        self.connect_button = tk.Button(self.frame, text="Connect", command=self.on_connect)
        self.connect_button.pack(pady=10)

        self.frame.pack()

        self.client = Client("ip-servidor-aqui", 50000)

    def on_connect(self):
        self.client.connect()
        self.on_connect_callback()
        

class AplicacaoBackup:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Programa de Backup")

        self.connection_screen = ConnectionScreen(janela, self.show_main_screen)
        self.client = self.connection_screen.client

    def show_main_screen(self):
        self.connection_screen.frame.pack_forget()  # Hide the connection screen
        self.botao_deposito = tk.Button(self.janela, text="Modo Depósito", command=self.modo_deposito)
        self.botao_deposito.pack(pady=10)

        self.botao_recuperacao = tk.Button(self.janela, text="Modo Recuperação", command=self.modo_recuperacao)
        self.botao_recuperacao.pack(pady=10)
        
        self.update_replication = tk.Button(self.janela, text="Modo Update", command=self.update_replication)
        self.update_replication.pack(pady=10)

        self.botao_desconect = tk.Button(self.janela, text="Desconectar", command=self.disconnect)
        self.botao_desconect.pack(pady=10)

    def modo_deposito(self):
        filename = filedialog.askopenfilename(title="Selecione o arquivo para depósito")
        filename = filename.split('/')[-1]
        if filename:
            q_replicas = tk.simpledialog.askinteger("Tolerância de Falhas", "Informe a tolerância de falhas:")
            if q_replicas is not None:
                try:
                    q_replicas = int(q_replicas)
                    self.client.deposit(filename, q_replicas)
                    print(f"Arquivo selecionado: {filename}")
                    print(f"Tolerância de falhas: {q_replicas}")
                except:
                    print("Valor inválido")

        

    def modo_recuperacao(self):
        filename = tk.simpledialog.askstring("Modo Recuperação", "Digite o nome do arquivo para recuperação:")
        if filename:
            self.client.recover(filename)
            print(f"Nome do arquivo selecionado para recuperação: {filename}")

    def update_replication(self):
        filename = tk.simpledialog.askstring("Modo Recuperação", "Digite o nome do arquivo para modificar tolerancia:")
        if filename:
            q_replicas = tk.simpledialog.askinteger("Tolerância de Falhas", "Informe a tolerância de falhas:")
            if q_replicas is not None:
                try:
                    q_replicas = int(q_replicas)
                    self.client.update_replication(filename, q_replicas)
                    print(f"Arquivo selecionado: {filename}")
                    print(f"Tolerância de falhas: {q_replicas}")
                except:
                    print("Valor inválido")
    
    def disconnect(self):
        self.client.close()
        self.janela.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoBackup(root)
    root.mainloop()
