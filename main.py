import cv2
import time
import threading
from collections import deque
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContentSettings
import os
import serial

# CONFIGURAÇÕES
FPS = 30
BUFFER_SECONDS = 30
MAX_FRAMES = FPS * BUFFER_SECONDS

# Blob Storage

ACCOUNT_URL = "https://passabola.blob.core.windows.net"
SAS_TOKEN = "sp=racwdl&st=2025-11-04T02:19:01Z&se=2025-11-11T02:59:00Z&sv=2024-11-04&sr=c&sig=imZh4MPAGROOoGp2VukPsRzdIhcIHR9Ak%2Bpl33uQ87s%3D"

blob_service_client = BlobServiceClient(account_url=ACCOUNT_URL, credential=SAS_TOKEN)
container_client = blob_service_client.get_container_client("videos")
containerName = "videos"

# Conexão ESP32
SERIAL_PORT = "COM5"       #Porta padrão 5
BAUD_RATE = 115200

# Câmera e buffer circular
buffer = deque(maxlen=MAX_FRAMES)
cap = cv2.VideoCapture(0)

# Flag de controle
gravar_clipe = False


# FUNÇÕES PRINCIPAIS
def capturar_frames():
    """Captura continuamente os frames da webcam e guarda no buffer."""
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        buffer.append(frame)
        time.sleep(1 / FPS)


def salvar_e_enviar_video():
    """Salva os frames do buffer em um arquivo e envia pro Azure Blob."""
    global gravar_clipe

    while True:
        if gravar_clipe:
            gravar_clipe = False

            if len(buffer) == 0:
                print("Nenhum frame no buffer, pulando...")
                continue

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"clip_{timestamp}.mp4"
            filepath = os.path.join(".", filename)

            height, width, _ = buffer[0].shape
            fourcc = cv2.VideoWriter_fourcc(*"X264")
            out = cv2.VideoWriter(filepath, fourcc, FPS, (width, height))

            for frame in list(buffer):
                out.write(frame)
            out.release()

            print(f"Vídeo salvo localmente: {filename}")

            # Envia pro Azure Blob
            try:
                with open(filepath, "rb") as data:
                    container_client.upload_blob(
                        name=filename,
                        data=data,
                        overwrite=True,
                        content_settings=ContentSettings(
                            content_type="video/mp4",
                            content_disposition="inline"
                        )
                )   

                blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{containerName}/{filename}"
                print(f"Upload concluído!\nURL: {blob_url}")

            except Exception as e:
                print(f"!!!Erro ao enviar pro Blob: {e} !!!")

            os.remove(filepath)

        time.sleep(0.1)


def escutarSerial():
    global gravar_clipe


    while True:
        if ser.in_waiting > 0:
            linha = ser.readline().decode().strip()
            if linha:
                print(f"[Serial] Recebido: {linha}")

                if linha.upper() in ["BOTAO", "TRIGGER", "1", "ON"]:
                    print("Sinal do ESP32 recebido, salvando clipe...")
                    gravar_clipe = True


# EXECUÇÃO
if __name__ == "__main__":
    t1 = threading.Thread(target=capturar_frames, daemon=True)
    t2 = threading.Thread(target=salvar_e_enviar_video, daemon=True)
    t3 = threading.Thread(target=escutar_serial, daemon=True)


    t1.start()
    t2.start()
    t3.start()

    print("Sistema iniciado. Aguardando sinal do ESP32 via serial...")


    try:        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
            print("Ocorreu um erro, encerrando...")
    finally:
        cap.release()
        ser.close()
        print("Encerrado com segurança.")
