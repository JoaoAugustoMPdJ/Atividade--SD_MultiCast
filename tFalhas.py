import sqlite3
import time

# Conectar ao banco SQLite
conn = sqlite3.connect("checkpoint.db")
cursor = conn.cursor()

# Criar tabela de mensagens
cursor.execute("""
CREATE TABLE IF NOT EXISTS mensagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conteudo TEXT
)
""")
conn.commit()

# Função para salvar mensagens
def salvar_mensagem(mensagem):
    cursor.execute("INSERT INTO mensagens (conteudo) VALUES (?)", (mensagem,))
    conn.commit()
    print(f"Checkpoint salvo: {mensagem}")

# Função para recuperar estado após falha
def recuperar_mensagens():
    cursor.execute("SELECT conteudo FROM mensagens")
    mensagens = cursor.fetchall()
    print("\nRecuperando mensagens após falha...")
    for mensagem in mensagens:
        print(f"Mensagem: {mensagem[0]}")

# Simulação de envio de mensagens com falha
try:
    salvar_mensagem("Mensagem 1")
    time.sleep(2)
    salvar_mensagem("Mensagem 2")
    time.sleep(2)
    1 / 0  # Simula uma falha no sistema
except Exception as e:
    print(f"Falha detectada: {e}")
    recuperar_mensagens()
