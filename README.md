Com certeza! Baseado nos arquivos que você enviou e no contexto da "Passa a Bola", aqui está uma sugestão de README.md seguindo o estilo que você pediu.

:clapper: Botão de Clipe - Passa a Bola
Sistema de Captura de Melhores Momentos com ESP32 e Azure
Este projeto utiliza uma webcam conectada a um script Python para gravar continuamente os últimos segundos de vídeo em um buffer. Ao receber um sinal de um botão físico (via ESP32), o sistema salva esse buffer como um clipe .mp4 e o envia automaticamente para o Azure Blob Storage, disponibilizando-o para a aplicação web da "Passa a Bola".

:pencil: Descrição do Problema
Em ambientes esportivos como quadras, campos e outros locais de prática, capturar o exato momento de um lance incrível (um gol, uma cesta, um drible) é um desafio. Gravar o tempo todo gera horas de material de vídeo inútil e de difícil análise, enquanto iniciar a gravação manualmente muitas vezes resulta na perda do início da jogada.

Para a "Passa a Bola", que foca em fornecer esses momentos aos seus usuários, é necessário um sistema que reaja instantaneamente após o evento ocorrer, garantindo que o "melhor momento" seja capturado na íntegra.Com certeza! Baseado nos arquivos que você enviou e no contexto da "Passa a Bola", aqui está uma sugestão de README.md seguindo o estilo que você pediu.

:clapper: Botão de Clipe - Passa a Bola
Sistema de Captura de Melhores Momentos com ESP32 e Azure
Este projeto utiliza uma webcam conectada a um script Python para gravar continuamente os últimos segundos de vídeo em um buffer. Ao receber um sinal de um botão físico (via ESP32), o sistema salva esse buffer como um clipe .mp4 e o envia automaticamente para o Azure Blob Storage, disponibilizando-o para a aplicação web da "Passa a Bola".

:pencil: Descrição do Problema
Em ambientes esportivos como quadras, campos e outros locais de prática, capturar o exato momento de um lance incrível (um gol, uma cesta, um drible) é um desafio. Gravar o tempo todo gera horas de material de vídeo inútil e de difícil análise, enquanto iniciar a gravação manualmente muitas vezes resulta na perda do início da jogada.

Para a "Passa a Bola", que foca em fornecer esses momentos aos seus usuários, é necessário um sistema que reaja instantaneamente após o evento ocorrer, garantindo que o "melhor momento" seja capturado na íntegra.

:bulb: Visão Geral da Solução
O sistema implementado (visto em main.py) resolve este problema através de uma gravação em buffer circular.

Uma câmera (webcam) filma continuamente, mas o script armazena apenas os últimos 15 segundos de frames em memória. Um botão físico, conectado a um microcontrolador ESP32, atua como um gatilho.

Quando o botão é pressionado, o ESP32 envia um sinal ("ON") via porta serial para o computador. O script Python detecta esse sinal, para de gravar o buffer e imediatamente salva os frames armazenados (os 15 segundos anteriores ao clique) em um arquivo de vídeo .mp4.

Este arquivo é então enviado para um container no Azure Blob Storage, pronto para ser acessado pela aplicação web da Passa a Bola.

:wrench: Componentes Utilizados
Hardware

ESP32 Microcontrolador responsável por ler o estado do botão e enviar um sinal via comunicação serial.

Botão (Push Button) O gatilho físico que o usuário (ou árbitro, ou jogador) pressiona para salvar um clipe.

Webcam (ou Câmera USB) Dispositivo de captura de vídeo conectado ao computador que executa o script Python (cv2.VideoCapture(0)).

Software e Serviços

Python (Script Principal) O núcleo do sistema (main.py), que gerencia a captura de vídeo, o buffer, a escuta serial e o upload para a nuvem usando threading.

Azure Blob Storage Serviço de nuvem da Microsoft utilizado para armazenar os clipes de vídeo gerados de forma segura e escalável.

OpenCV (cv2) Biblioteca utilizada para a captura e processamento dos frames de vídeo.

Com certeza! Baseado nos arquivos que você enviou e no contexto da "Passa a Bola", aqui está uma sugestão de README.md seguindo o estilo que você pediu.

:clapper: Botão de Clipe - Passa a Bola
Sistema de Captura de Melhores Momentos com ESP32 e Azure
Este projeto utiliza uma webcam conectada a um script Python para gravar continuamente os últimos segundos de vídeo em um buffer. Ao receber um sinal de um botão físico (via ESP32), o sistema salva esse buffer como um clipe .mp4 e o envia automaticamente para o Azure Blob Storage, disponibilizando-o para a aplicação web da "Passa a Bola".

:pencil: Descrição do Problema
Em ambientes esportivos como quadras, campos e outros locais de prática, capturar o exato momento de um lance incrível (um gol, uma cesta, um drible) é um desafio. Gravar o tempo todo gera horas de material de vídeo inútil e de difícil análise, enquanto iniciar a gravação manualmente muitas vezes resulta na perda do início da jogada.

Para a "Passa a Bola", que foca em fornecer esses momentos aos seus usuários, é necessário um sistema que reaja instantaneamente após o evento ocorrer, garantindo que o "melhor momento" seja capturado na íntegra.

:bulb: Visão Geral da Solução
O sistema implementado (visto em main.py) resolve este problema através de uma gravação em buffer circular.

Uma câmera (webcam) filma continuamente, mas o script armazena apenas os últimos 15 segundos de frames em memória. Um botão físico, conectado a um microcontrolador ESP32, atua como um gatilho.

Quando o botão é pressionado, o ESP32 envia um sinal ("ON") via porta serial para o computador. O script Python detecta esse sinal, para de gravar o buffer e imediatamente salva os frames armazenados (os 15 segundos anteriores ao clique) em um arquivo de vídeo .mp4.

Este arquivo é então enviado para um container no Azure Blob Storage, pronto para ser acessado pela aplicação web da Passa a Bola.

:wrench: Componentes Utilizados
Hardware

ESP32 Microcontrolador responsável por ler o estado do botão e enviar um sinal via comunicação serial.

Botão (Push Button) O gatilho físico que o usuário (ou árbitro, ou jogador) pressiona para salvar um clipe.

Webcam (ou Câmera USB) Dispositivo de captura de vídeo conectado ao computador que executa o script Python (cv2.VideoCapture(0)).

Software e Serviços

Python (Script Principal) O núcleo do sistema (main.py), que gerencia a captura de vídeo, o buffer, a escuta serial e o upload para a nuvem usando threading.

Azure Blob Storage Serviço de nuvem da Microsoft utilizado para armazenar os clipes de vídeo gerados de forma segura e escalável.

OpenCV (cv2) Biblioteca utilizada para a captura e processamento dos frames de vídeo.

:gear: Funcionamento
O script main.py é executado, iniciando três threads (processos paralelos):

capturar_frames: Conecta-se à webcam e salva os frames continuamente em um deque (buffer circular) com capacidade para 15 segundos (FPS * BUFFER_SECONDS).

escutarSerial: Monitora a porta serial (ex: COM3) aguardando dados.

salvar_e_enviar_video: Aguarda a ativação da flag gravar_clipe.

Enquanto isso, o ESP32 monitora o pino do botão (BOTAO_PIN 32).

Quando o botão é pressionado, seu estado vai para LOW. O ESP32 detecta isso e envia a string "ON" pela porta serial.

A thread escutarSerial (em main.py) recebe a string "ON" (ou "BOTAO", "TRIGGER", "1") e imediatamente define a flag global gravar_clipe como True.

A thread salvar_e_enviar_video detecta a mudança na flag. Ela pega a lista atual de frames do buffer e usa o cv2.VideoWriter para compilar um arquivo .mp4 (com codec X264).

O arquivo é nomeado com um timestamp (ex: clip_2025-11-07_10-00-00.mp4).

O script faz o upload desse arquivo para o container "videos" no Azure Blob Storage, usando as credenciais (ACCOUNT_URL e SAS_TOKEN).

Após o upload bem-sucedido, o arquivo de vídeo local é removido (os.remove(filepath)) para economizar espaço em disco.

O sistema continua gravando o buffer e aguardando o próximo clique.
Com certeza! Baseado nos arquivos que você enviou e no contexto da "Passa a Bola", aqui está uma sugestão de README.md seguindo o estilo que você pediu.

:clapper: Botão de Clipe - Passa a Bola
Sistema de Captura de Melhores Momentos com ESP32 e Azure
Este projeto utiliza uma webcam conectada a um script Python para gravar continuamente os últimos segundos de vídeo em um buffer. Ao receber um sinal de um botão físico (via ESP32), o sistema salva esse buffer como um clipe .mp4 e o envia automaticamente para o Azure Blob Storage, disponibilizando-o para a aplicação web da "Passa a Bola".

:pencil: Descrição do Problema
Em ambientes esportivos como quadras, campos e outros locais de prática, capturar o exato momento de um lance incrível (um gol, uma cesta, um drible) é um desafio. Gravar o tempo todo gera horas de material de vídeo inútil e de difícil análise, enquanto iniciar a gravação manualmente muitas vezes resulta na perda do início da jogada.

Para a "Passa a Bola", que foca em fornecer esses momentos aos seus usuários, é necessário um sistema que reaja instantaneamente após o evento ocorrer, garantindo que o "melhor momento" seja capturado na íntegra.

:bulb: Visão Geral da Solução
O sistema implementado (visto em main.py) resolve este problema através de uma gravação em buffer circular.

Uma câmera (webcam) filma continuamente, mas o script armazena apenas os últimos 15 segundos de frames em memória. Um botão físico, conectado a um microcontrolador ESP32, atua como um gatilho.

Quando o botão é pressionado, o ESP32 envia um sinal ("ON") via porta serial para o computador. O script Python detecta esse sinal, para de gravar o buffer e imediatamente salva os frames armazenados (os 15 segundos anteriores ao clique) em um arquivo de vídeo .mp4.

Este arquivo é então enviado para um container no Azure Blob Storage, pronto para ser acessado pela aplicação web da Passa a Bola.

:wrench: Componentes Utilizados
Hardware

ESP32 Microcontrolador responsável por ler o estado do botão e enviar um sinal via comunicação serial.

Botão (Push Button) O gatilho físico que o usuário (ou árbitro, ou jogador) pressiona para salvar um clipe.

Webcam (ou Câmera USB) Dispositivo de captura de vídeo conectado ao computador que executa o script Python (cv2.VideoCapture(0)).

Software e Serviços

Python (Script Principal) O núcleo do sistema (main.py), que gerencia a captura de vídeo, o buffer, a escuta serial e o upload para a nuvem usando threading.

Azure Blob Storage Serviço de nuvem da Microsoft utilizado para armazenar os clipes de vídeo gerados de forma segura e escalável.

OpenCV (cv2) Biblioteca utilizada para a captura e processamento dos frames de vídeo.

:gear: Funcionamento
O script main.py é executado, iniciando três threads (processos paralelos):

capturar_frames: Conecta-se à webcam e salva os frames continuamente em um deque (buffer circular) com capacidade para 15 segundos (FPS * BUFFER_SECONDS).

escutarSerial: Monitora a porta serial (ex: COM3) aguardando dados.

salvar_e_enviar_video: Aguarda a ativação da flag gravar_clipe.

Enquanto isso, o ESP32 monitora o pino do botão (BOTAO_PIN 32).

Quando o botão é pressionado, seu estado vai para LOW. O ESP32 detecta isso e envia a string "ON" pela porta serial.

A thread escutarSerial (em main.py) recebe a string "ON" (ou "BOTAO", "TRIGGER", "1") e imediatamente define a flag global gravar_clipe como True.

A thread salvar_e_enviar_video detecta a mudança na flag. Ela pega a lista atual de frames do buffer e usa o cv2.VideoWriter para compilar um arquivo .mp4 (com codec X264).

O arquivo é nomeado com um timestamp (ex: clip_2025-11-07_10-00-00.mp4).

O script faz o upload desse arquivo para o container "videos" no Azure Blob Storage, usando as credenciais (ACCOUNT_URL e SAS_TOKEN).

Após o upload bem-sucedido, o arquivo de vídeo local é removido (os.remove(filepath)) para economizar espaço em disco.

O sistema continua gravando o buffer e aguardando o próximo clique.

:tv: Visualização no Front-End
Os vídeos enviados para o Azure Blob Storage podem ser consumidos diretamente pela aplicação web da "Passa a Bola". O arquivo TesteFront.html demonstra um player de vídeo HTML simples que reproduz um clipe diretamente do blob, bastando fornecer a URL do arquivo e a SAS Token de acesso:

HTML

<video controls width="720" autoplay>
    <source src="https://passabola.blob.core.windows.net/videos/clip_2025-11-06_19-46-09.mp4?sp=racwd...[SAS_TOKEN]..." type="video/mp4">
    Seu navegador não suporta a tag de vídeo.
</video>

:electric_plug: Diagrama de Conexão

Componente,Conexão,Pino/Porta
Botão (Saída),ESP32 (Entrada),Pino 32
Botão (Outro lado),ESP32 (GND),GND
ESP32 (USB),PC (Host),COM3 (exemplo)
Webcam,PC (Host),USB

📚 Bibliotecas
Python (main.py)

cv2 (opencv-python)

time

threading

collections.deque

datetime

azure.storage.blob

os

serial (pyserial)

Arduino (serial.c)

Arduino.h