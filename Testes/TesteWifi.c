#include <WiFi.h>
#include <WebServer.h>

// Nome da Rede: ESP32_BOTAO
// Senha: 12345678

WebServer server(80);

// Estado do botão virtual
bool botaoVirtual = false;

// Página principal com botão
void handleRoot() {
  String html = 
    "<html>"
    "<head>"
    "<meta name='viewport' content='width=device-width, initial-scale=1'/>"
    "<style>"
    "body { font-family: Arial; text-align:center; padding-top:50px; }"
    "button { font-size: 30px; padding: 20px 40px; border-radius: 15px; cursor:pointer; }"
    "</style>"
    "</head>"
    "<body>"
    "<h1>Controle do ESP32</h1>"
    "<button onclick=\"fetch('/on')\" style='background:green;color:white;'>LIGAR</button>"
    "<br><br>"
    "<button onclick=\"fetch('/off')\" style='background:red;color:white;'>DESLIGAR</button>"
    "</body>"
    "</html>";

  server.send(200, "text/html", html);
}

void handleOn() {
  botaoVirtual = true;
  server.send(200, "text/plain", "ON");
  Serial.println("ON");  // Aqui você coloca a lógica que antes estava no botão físico
}

void handleOff() {
  botaoVirtual = false;
  server.send(200, "text/plain", "OFF");
  Serial.println("OFF");
}

void setup() {
  Serial.begin(115200);

  // Cria um Wi-Fi próprio no ESP32
  WiFi.softAP("ESP32_BOTAO", "12345678");
  Serial.println("Abra no navegador: http://192.168.4.1");

  // Rotas da página
  server.on("/", handleRoot);
  server.on("/on", handleOn);
  server.on("/off", handleOff);

  server.begin();
}

void loop() {
  server.handleClient();
}

