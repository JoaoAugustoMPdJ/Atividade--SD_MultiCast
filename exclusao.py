import time
import threading

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.has_token = (node_id == 0)  # O primeiro nó inicia com o token
        self.condition = threading.Condition()  # Controle de espera

    def request_access(self):
        global queue
        with self.condition:
            queue.append(self.node_id)  # Nó entra na fila
            print(f"Nó {self.node_id} solicitou acesso ao recurso.")

            while not self.has_token or queue[0] != self.node_id:
                self.condition.wait()  # Espera até ser o primeiro da fila e ter o token

            print(f"Nó {self.node_id} obteve acesso ao recurso!")
            time.sleep(2)  # Simula o uso do recurso
            self.release_access()

    def release_access(self):
        global queue, nodes
        with self.condition:
            print(f"Nó {self.node_id} liberou o acesso ao recurso.")

            queue.pop(0)  # Remove o nó atual da fila
            self.has_token = False

            # Passa o token para o próximo nó na fila
            if queue:
                next_node_id = queue[0]
                nodes[next_node_id].has_token = True
                print(f"Token passado para o Nó {next_node_id}")

                # Notifica o próximo nó
                with nodes[next_node_id].condition:
                    nodes[next_node_id].condition.notify()
            else:
                print("Nenhum nó na fila. O recurso está disponível.")

def node_simulation(node):
    while True:
        time.sleep(node.node_id + 1)  # Evita solicitações simultâneas
        node.request_access()

if __name__ == "__main__":
    total_nodes = 3
    nodes = [Node(i) for i in range(total_nodes)]
    
    queue = []  # Fila compartilhada entre os nós

    threads = []
    for node in nodes:
        t = threading.Thread(target=node_simulation, args=(node,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
