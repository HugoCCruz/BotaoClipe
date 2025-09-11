import cv2
import time
import threading
from collections import deque
from datetime import datetime
from flask import Flask, jsonify

# Configurações do vídeo
FPS = 30
BUFFER_SECONDS = 30
MAX_FRAMES = FPS * BUFFER_SECONDS

# Cria o buffer circular para armazenar os frames
buffer = deque(maxlen=MAX_FRAMES)

# Inicializa a webcam
cap = cv2.VideoCapture(0)

# Inicializa o servidor Flask
app = Flask(__name__)

# Função que captura os frames da webcam em uma thread separada
def capture_frames():
    """Captura frames da webcam e os armazena no buffer."""
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        buffer.append(frame)

# Função que salva o clipe de vídeo localmente
def save_clip():
    """Salva o clipe de vídeo do buffer e retorna o status."""
    
    # Verifica se há frames suficientes no buffer
    if len(buffer) == 0:
        return {"status": "error", "message": "Sem frames suficientes no buffer"}

    # Cria uma cópia segura do buffer para evitar conflitos
    frames = list(buffer)
    
    try:
        height, width, _ = frames[0].shape
        
        # Cria um nome de arquivo único com a data e hora
        now = datetime.now()
        filename = now.strftime("clip_%Y-%m-%d_%H-%M-%S.mp4")

        # Cria e salva o arquivo de vídeo
        out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), FPS, (width, height))
        for frame in frames:
            out.write(frame)
        out.release()
        
        print(f"✅ Clipe salvo como {filename}")
        return {"status": "success", "message": f"Clipe salvo como {filename}"}

    except Exception as e:
        print(f"❌ Erro ao salvar o clipe: {e}")
        return {"status": "error", "message": f"Erro ao salvar o clipe: {e}"}

# Rota da API que o ESP32 irá chamar
@app.route("/save", methods=['GET'])
def save_and_respond():
    """Recebe a requisição do ESP32, salva o clipe e retorna um JSON."""
    result = save_clip()
    return jsonify(result)

# Bloco principal para iniciar o programa
if __name__ == "__main__":
    # Inicia a thread de captura de frames em segundo plano
    t = threading.Thread(target=capture_frames, daemon=True)
    t.start()
    
    # Inicia o servidor Flask, ouvindo todas as interfaces de rede na porta 5000
    print("Servidor rodando e pronto para receber requisições do ESP32.")
    print("Pressione CTRL+C para sair.")
    app.run(host="0.0.0.0", port=5000)