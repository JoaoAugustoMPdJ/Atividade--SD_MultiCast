import socket
import struct
import threading
import datetime

# Configurações do grupo multicast
MULTICAST_GROUP = '224.1.1.1'
PORT = 5007
BUFFER_SIZE = 1024

def receive_messages(sock):    # Função para receber mensagens do grupo multicast
   
    while True:
        try:
            data, sender = sock.recvfrom(BUFFER_SIZE)
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")  # Captura o horário atual
            sender_ip = sender[0]  # Captura o endereço IP do remetente

            print(f"\n[{timestamp}] ({sender_ip}): {data.decode('utf-8')}")
        except Exception as e:
            print("Erro ao receber mensagem:", e)
            break

def main():
    # Criar o socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Permitir reutilização do endereço para múltiplos clientes
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Associar o socket à porta
    sock.bind(('', PORT))

    # Entrar no grupo multicast
    mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Criar uma thread para receber mensagens
    thread = threading.Thread(target=receive_messages, args=(sock,))
    thread.daemon = True
    thread.start()

    print("=== Chat Multicast ===")
    print("Digite mensagens para enviar ao grupo.\n")

    while True:
        try:
            # Ler mensagem do usuário
            message = input("> ")
            if not message:
                continue

            # Enviar mensagem para o grupo multicast
            sock.sendto(message.encode('utf-8'), (MULTICAST_GROUP, PORT))
        except KeyboardInterrupt:
            print("\nSaindo do chat...")
            break

    sock.close()

if __name__ == "__main__":
    main()
