import cv2
import time
import threading
from collections import deque
from datetime import datetime
from azure.storage.blob import BlobServiceClient
import os
import serial

# CONFIGURAÇÕES
SERIAL_PORT = "COM5"       # Porta de conexão com o ESP32
BAUD_RATE = 115200

# Câmera
FPS = 30
BUFFER_SECONDS = 30
MAX_FRAMES = FPS * BUFFER_SECONDS

# Blob Storage
CONNECTION_STRING = "BlobEndpoint=https://passabola.blob.core.windows.net/;QueueEndpoint=https://passabola.queue.core.windows.net/;FileEndpoint=https://passabola.file.core.windows.net/;TableEndpoint=https://passabola.table.core.windows.net/;SharedAccessSignature=sv=2024-11-04&ss=b&srt=sco&sp=rlctfx&se=2025-10-21T03:00:00Z&st=2025-10-21T02:34:57Z&spr=https&sig=FNMWrCR%2FUclps2f41AoyR69DLKfznPwClD2EZQgZxBA%3D"
CONTAINER_NAME = "videos"

# INICIALIZAÇÕES

# Blob
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# # Câmera e gravação contínua
# buffer = deque(maxlen=MAX_FRAMES)
# cap = cv2.VideoCapture(0)

# Conecta à serial pro ESP32
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
print(f"Conectado à {SERIAL_PORT}")

# Flag de controle
gravar_clipe = False


# # FUNÇÕES PRINCIPAIS
# def capturar_frames():
#     # Captura continuamente os frames da webcam e guarda no buffer
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             continue
#         buffer.append(frame)
#         time.sleep(1 / FPS)


def salvar_e_enviar_video():
    # Salva os frames do buffer em um arquivo e envia pro Azure Blob
    global gravar_clipe

    while True:
        if gravar_clipe:
            gravar_clipe = False

            # if len(buffer) == 0:
            #     print("Nenhum frame no buffer, pulando...")
            #     continue

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"clip_{timestamp}.mp4"
            filepath = os.path.join(".", filename)

            height, width, _ = buffer[0].shape
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(filepath, fourcc, FPS, (width, height))

            for frame in list(buffer):
                out.write(frame)
            out.release()

            print(f"🎬 Vídeo salvo localmente: {filename}")

            # Envia pro Azure Blob
            try:
                with open(filepath, "rb") as data:
                    container_client.upload_blob(name=filename, data=data, overwrite=True)

                blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{filename}"
                print(f"☁️  Upload concluído!\n🔗 URL: {blob_url}")

            except Exception as e:
                print(f"❌ Erro ao enviar pro Blob: {e}")

            os.remove(filepath)


def escutar_serial():
    # Escuta a serial e aciona a gravação quando o ESP32 envia sinal
    global gravar_clipe

    while True:
        if ser.in_waiting > 0:
            linha = ser.readline().decode().strip()
            if linha:
                print(f"[Serial] Recebido: {linha}")

                if linha.upper() in ["BOTAO", "TRIGGER", "1"]:
                    print("🎯 Sinal do ESP32 recebido, salvando clipe...")
                    gravar_clipe = True


# EXECUÇÃO
if __name__ == "__main__":
    # t1 = threading.Thread(target=capturar_frames, daemon=True)
    t2 = threading.Thread(target=salvar_e_enviar_video, daemon=True)
    t3 = threading.Thread(target=escutar_serial, daemon=True)

    # t1.start()
    t2.start()
    t3.start()

    print("📹 Sistema iniciado. Aguardando sinal do ESP32 via serial...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # cap.release()
        ser.close()
        print("Encerrado com segurança.")