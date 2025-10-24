// ====== Bibliotecas ======
#include <Arduino.h>

// ====== Configurações ======
#define BOTAO_PIN  32          // Pino onde o botão está conectado 
#define DEBOUNCE_TIME 300     // Tempo de debounce (ms)

// ====== Variáveis ======
unsigned long ultimoPress = 0;

void setup() {
  // Inicializa comunicação serial
  Serial.begin(115200);
  delay(1000); // Pequeno atraso para estabilizar a porta serial

  // Configura o pino do botão
  pinMode(BOTAO_PIN, INPUT_PULLUP); // botão entre pino e GND

  Serial.println("ESP32 pronto. Aguardando pressionamento do botão...");
}

void loop() {
  int estadoBotao = digitalRead(BOTAO_PIN);

  // Verifica se o botão foi pressionado (nível LOW)
  if (estadoBotao == LOW) {
    unsigned long agora = millis();
    Serial.println("ON");

    // Verifica debounce
    if (agora - ultimoPress > DEBOUNCE_TIME) {
      ultimoPress = agora;

      // Feedback opcional (LED interno ou serial)
      // Serial.println("📤 Sinal enviado ao PC!");
    }
  } else {
    Serial.println("OFF");
  }

  delay(500); // Evita leituras muito rápidas
}
