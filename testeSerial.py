import serial
import time

# Configurações da porta serial
porta = 'COM5'        # No Windows (ex: COM3)
# porta = '/dev/ttyUSB0'  # No Linux
baud_rate = 115200       # Taxa de transmissão (mesma do dispositivo)
timeout = 1            # Tempo máximo de espera por leitura (em segundos)

# Abre a conexão serial
ser = serial.Serial(porta, baud_rate, timeout=timeout)
time.sleep(2)  # Aguarda estabilização da conexão

print(f"Conectado à porta {porta}")

try:
    while True:
        if ser.in_waiting > 0:  # Verifica se há dados disponíveis
            linha = ser.readline().decode('utf-8').strip()
            print(f"Dado recebido: {linha}")
except KeyboardInterrupt:
    print("\nLeitura interrompida pelo usuário.")
finally:
    ser.close()
    print("Conexão serial encerrada.")
