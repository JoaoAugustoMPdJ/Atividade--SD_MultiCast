import time
import threading
import random

# Configuração
REPLICAS = ["replica1.txt", "replica2.txt", "replica3.txt"]
DELAY_RANGE = (1, 5)  # Simulação de entrega fora de ordem

def inicializar_replicas(): # Cria arquivos de réplica vazios.
    
    for replica in REPLICAS:
        open(replica, 'w').close()

def escrever_mensagem(mensagem):    # Escreve a mensagem em réplicas com delay artificial.

    def escrever(replica):
        time.sleep(random.randint(*DELAY_RANGE))  # Simula entrega fora de ordem
        with open(replica, 'a') as f:
            f.write(mensagem + "\n")
        print(f"Mensagem '{mensagem}' escrita em {replica}")
    
    threads = [threading.Thread(target=escrever, args=(r,)) for r in REPLICAS]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

def reconciliador():     # Sincroniza as réplicas garantindo consistência eventual.

    mensagens = set()
    for replica in REPLICAS:
        with open(replica, 'r') as f:
            mensagens.update(f.readlines())
    
    for replica in REPLICAS:
        with open(replica, 'w') as f:
            f.writelines(mensagens)
    print("Réplicas sincronizadas!")

def demonstracao():     # Executa a demonstração do processo de replicação e reconciliação.

    inicializar_replicas()
    mensagens = ["Olá", "Mundo", "Primeiro", "Segundo"]
    
    print("--- Iniciando replicação ---")
    for msg in mensagens:
        escrever_mensagem(msg)
    
    print("\n--- Estado das réplicas antes da reconciliação ---")
    for replica in REPLICAS:
        with open(replica, 'r') as f:
            print(f"{replica}: {f.readlines()}")
    
    print("\n--- Executando reconciliador ---")
    reconciliador()
    
    print("\n--- Estado final das réplicas ---")
    for replica in REPLICAS:
        with open(replica, 'r') as f:
            print(f"{replica}: {f.readlines()}")

if __name__ == "__main__":
    demonstracao()
