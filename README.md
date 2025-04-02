# Sistemas Distribuídos

Discentes: João Augusto Moura Peixoto de Jesus (20211TADSSAJ0004) e Gustavo Vitor Oliveira de Andrade (20221TADSSAJ0003)

## Introdução  
Este repositório contém quatro implementações relacionadas a conceitos fundamentais de sistemas distribuídos:  
1. **Chat Multicast**  
2. **Replicação e Reconciliação de Dados**  
3. **Controle de Acesso Distribuído com Token**  
4. **Checkpoint e Recuperação de Falha**  

Cada um desses códigos aborda desafios comuns em sistemas distribuídos, como comunicação entre múltiplos nós, consistência de dados, sincronização de acesso e tolerância a falhas.  

## 1. Chat Multicast  
**Objetivo:** Criar um chat distribuído utilizando multicast UDP, permitindo que múltiplos clientes se comuniquem em um grupo.  

### Conceitos Aplicados  
- **Comunicação Multicast:** Permite que uma mensagem seja enviada para um grupo de nós ao mesmo tempo.  
- **Sockets UDP:** Protocolo leve e sem conexão, ideal para transmissão rápida de mensagens.  
- **Threads:** Utilizadas para escutar mensagens enquanto permite que o usuário envie outras.  

### Desafios  
- **Fiabilidade:** Como o UDP não garante entrega de pacotes, mensagens podem ser perdidas.  
- **Segurança:** O multicast não possui criptografia embutida, tornando a comunicação vulnerável.  

## 2. Replicação e Reconciliação de Dados  
**Objetivo:** Implementar um sistema de replicação de arquivos que garante consistência eventual entre diferentes réplicas.  

### Conceitos Aplicados  
- **Replicação de Dados:** Cada mensagem é armazenada em múltiplas réplicas para redundância.  
- **Consistência Eventual:** As mensagens podem ser escritas em momentos diferentes, mas um reconciliador garante que todas fiquem idênticas no final.  
- **Simulação de Delay:** Introduz uma latência artificial para simular entrega fora de ordem.  

### Desafios  
- **Entrega Fora de Ordem:** Como as mensagens são escritas com delays aleatórios, a ordem pode diferir entre réplicas.  
- **Reconciliador Eficiente:** Para garantir que todas as réplicas tenham as mesmas mensagens sem duplicatas.  

## 3. Controle de Acesso Distribuído com Token  
**Objetivo:** Implementar um sistema onde diferentes nós solicitam acesso a um recurso compartilhado e o controle é garantido por um token.  

### Conceitos Aplicados  
- **Mutua Exclusão Distribuída:** Garante que apenas um nó possa acessar o recurso de cada vez.  
- **Fila de Prioridade:** Os nós entram em uma fila para acessar o recurso de maneira ordenada.  
- **Passagem de Token:** O token é passado entre os nós, garantindo que cada um tenha sua vez.  

### Desafios  
- **Evitar Inanição:** O sistema precisa garantir que cada nó receba o token dentro de um tempo razoável.  
- **Falhas na Transmissão do Token:** Caso um nó falhe ao passar o token, o sistema pode travar.  

## 4. Checkpoint e Recuperação de Falha  
**Objetivo:** Implementar um sistema que salva mensagens em um banco de dados SQLite, permitindo recuperação após falhas.  

### Conceitos Aplicados  
- **Checkpointing:** Periodicamente, os estados das mensagens são salvos no banco.  
- **Recuperação de Estado:** Após uma falha, o sistema pode recuperar mensagens não processadas.  
- **Persistência com Banco de Dados:** Uso de SQLite para armazenar dados de forma durável.  

### Desafios  
- **Tolerância a Falhas:** O sistema precisa detectar falhas e se recuperar automaticamente.  
- **Evitar Registros Duplicados:** A recuperação deve garantir que mensagens não sejam processadas duas vezes.  

## Implementações e Explicações  

### Chat Multicast  

**Descrição:**  
Este código cria um **chat multicast** baseado em UDP, permitindo que vários usuários enviem e recebam mensagens dentro de um grupo multicast.  

```python
import socket
import struct
import threading
import datetime

MULTICAST_GROUP = '224.1.1.1'
PORT = 5007
BUFFER_SIZE = 1024

def receive_messages(sock):
    while True:
        try:
            data, sender = sock.recvfrom(BUFFER_SIZE)
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            sender_ip = sender[0]
            print(f"\n[{timestamp}] ({sender_ip}): {data.decode('utf-8')}")
        except Exception as e:
            print("Erro ao receber mensagem:", e)
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', PORT))

    mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    thread = threading.Thread(target=receive_messages, args=(sock,))
    thread.daemon = True
    thread.start()

    print("=== Chat Multicast ===\nDigite mensagens para enviar ao grupo.\n")

    while True:
        try:
            message = input("> ")
            if not message:
                continue
            sock.sendto(message.encode('utf-8'), (MULTICAST_GROUP, PORT))
        except KeyboardInterrupt:
            print("\nSaindo do chat...")
            break

    sock.close()

if __name__ == "__main__":
    main()
```
**Explicação:**  
- **Criação de socket UDP multicast** para comunicação entre múltiplos nós.  
- **Uso de threads** para recepção contínua de mensagens.  
- **Envio de mensagens para o grupo multicast**, permitindo que todos os membros recebam.  

---

### Replicação e Reconciliação de Dados  

```python
import time
import threading
import random

REPLICAS = ["replica1.txt", "replica2.txt", "replica3.txt"]
DELAY_RANGE = (1, 5)

def inicializar_replicas():
    for replica in REPLICAS:
        open(replica, 'w').close()

def escrever_mensagem(mensagem):
    def escrever(replica):
        time.sleep(random.randint(*DELAY_RANGE))
        with open(replica, 'a') as f:
            f.write(mensagem + "\n")
        print(f"Mensagem '{mensagem}' escrita em {replica}")
    
    threads = [threading.Thread(target=escrever, args=(r,)) for r in REPLICAS]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

def reconciliador():
    mensagens = set()
    for replica in REPLICAS:
        with open(replica, 'r') as f:
            mensagens.update(f.readlines())

    for replica in REPLICAS:
        with open(replica, 'w') as f:
            f.writelines(mensagens)
    print("Réplicas sincronizadas!")
```
**Explicação:**  
- **Simula a replicação eventual**, onde cada réplica pode receber mensagens em momentos diferentes.  
- **Uso de threads** para escrever em réplicas de forma concorrente.  
- **Reconciliador** sincroniza todas as réplicas para manter consistência.  


### Controle de Acesso Distribuído
 *Descrição*:
Este código implementa um algoritmo de passagem de token para coordenar o acesso a um recurso compartilhado.

*Código*:
```python
import threading
import time

token = threading.Semaphore(1)  # Token único

def acessar_recurso(id_processo):
    print(f"Processo {id_processo} esperando o token...")
    token.acquire()
    print(f"Processo {id_processo} acessando o recurso...")
    time.sleep(2)
    print(f"Processo {id_processo} liberando o token.")
    token.release()

threads = [threading.Thread(target=acessar_recurso, args=(i,)) for i in range(5)]

for t in threads:
    t.start()

for t in threads:
    t.join()
```
*Explicação*:
O programa cria um token (semaforo) que controla o acesso a um recurso compartilhado.

Vários processos aguardam sua vez para acessar o recurso.

Quando um processo termina, ele libera o token, permitindo que outro acesse.

*Conceitos aplicados*:
Passagem de token: Um nó tem permissão exclusiva para acessar um recurso.

Fila distribuída: Os nós aguardam sua vez para acessar o recurso.

### Recuperação Após Falha com Checkpoint

*Descrição*:
Este código salva mensagens em um banco SQLite para permitir recuperação após falha.

 *Código*:
```python
import sqlite3

con = sqlite3.connect("banco.db")
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS mensagens (msg TEXT)")

def salvar_mensagem(msg):
    cursor.execute("INSERT INTO mensagens VALUES (?)", (msg,))
    con.commit()

def recuperar_mensagens():
    cursor.execute("SELECT * FROM mensagens")
    return cursor.fetchall()

mensagens = ["Oi", "Teste", "Persistência"]
for m in mensagens:
    salvar_mensagem(m)

print("Mensagens recuperadas:", recuperar_mensagens())
```
*Explicação*:
As mensagens são salvas em um banco de dados SQLite.

Em caso de falha, as mensagens podem ser recuperadas do banco.

*Conceitos aplicados*:
Checkpointing: Salva o estado do sistema periodicamente.

Recuperação de falha: Após erro, as mensagens são restauradas.


---

## Conclusão  
Os quatro sistemas implementados abordam desafios comuns em sistemas distribuídos. Cada implementação serve como um exemplo prático dos conceitos teóricos apresentados, ajudando a compreender melhor como resolver problemas reais nesse tipo de ambiente.  

