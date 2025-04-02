import sqlite3
import time

# Função para conectar ao banco
def conectar_banco():
    return sqlite3.connect("checkpoint.db")

# Criar tabela no banco
conn = conectar_banco()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS mensagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conteudo TEXT
)
""")
conn.commit()
conn.close()

# Função para salvar mensagens
def salvar_mensagem(mensagem):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mensagens (conteudo) VALUES (?)", (mensagem,))
    conn.commit()
    conn.close()
    print(f"Checkpoint salvo: {mensagem}")

# Obtém o último ID salvo no banco
def get_ultimo_id():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM mensagens")
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado[0] else 0

# Função para recuperar mensagens após a falha
def recuperar_mensagens(ultimo_id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT id, conteudo FROM mensagens WHERE id > ?", (ultimo_id,))
    mensagens = cursor.fetchall()
    conn.close()

    if mensagens:
        print("\nRecuperando mensagens após falha...")
        for mid, mensagem in mensagens:
            print(f"Mensagem: {mensagem}")
        return mensagens[-1][0]  # Atualiza o último ID recuperado
    
    return ultimo_id

# Obtém o último ID antes de começar
ultimo_id = get_ultimo_id()

# Simulação de envio de mensagens com checkpoint
try:
    salvar_mensagem("Mensagem 1")
    time.sleep(2)

    salvar_mensagem("Mensagem 2")
    time.sleep(2)

    1 / 0  # Simula uma falha no sistema

except Exception as e:
    print(f"Falha detectada: {e}")

    # Recupera mensagens após a falha
    ultimo_id = recuperar_mensagens(ultimo_id)
