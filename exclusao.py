import socket
import threading
import json
import time

PORT = 5000
NODES = ["127.0.0.1:5001", "127.0.0.1:5002", "127.0.0.1:5003"]

class Node:
    def __init__(self, node_id, port):
        self.node_id = node_id
        self.port = port
        self.queue = []
        self.has_token = (node_id == 0)  # Apenas o primeiro nó inicia com o token

    def request_access(self):
        print(f"Nó {self.node_id} solicitando acesso ao recurso.")
        self.queue.append(self.node_id)
        self.check_access()

    def check_access(self):
        if self.has_token and self.queue and self.queue[0] == self.node_id:
            print(f"Nó {self.node_id} obteve acesso ao recurso!")
            time.sleep(2)  # Simula uso do recurso
            self.release_access()

    def release_access(self):
        print(f"Nó {self.node_id} liberando o recurso.")
        self.queue.pop(0)
        if self.queue:
            next_node = self.queue[0]
            print(f"Passando token para o Nó {next_node}")
            self.has_token = False
            # Aqui, deveria enviar o token para o próximo nó

    def run(self):
        while True:
            time.sleep(1)
            if self.node_id == 0:
                self.request_access()
            self.check_access()

if __name__ == "__main__":
    node = Node(node_id=0, port=PORT)
    node.run()
