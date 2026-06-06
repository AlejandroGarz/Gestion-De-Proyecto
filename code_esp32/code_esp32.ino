#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include "credentials.h"

//#include <ESP32Servo.h>

// OLED
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// WiFi
const char* ssid = WIFI_SSID;
const char* password = WIFI_PASSWORD;
const char* mqtt_server = MQTT_SERVER;
WiFiClient espClient;
PubSubClient client(espClient);

// Servo
//Servo servo;
//define PIN_SERVO 48  // cambia al pin que uses

#define LED_DISPENSAR 48

// cuando llega mensaje MQTT
void callback(char* topic, byte* payload, unsigned int length) {
    String mensaje = "";
    for (int i = 0; i < length; i++) {
        mensaje += (char)payload[i];
    }

    Serial.println("Topic: " + String(topic));
    Serial.println("Mensaje: " + mensaje);

    // muestra token en OLED
    if(String(topic) == "maquina/token") {
        display.clearDisplay();
        display.setTextSize(2);
        display.setTextColor(SSD1306_WHITE);
        display.setCursor(0, 10);
        display.println("Token:");
        display.setTextSize(3);
        display.setCursor(20, 35);
        display.println(mensaje);
        display.display();
    }

    if(String(topic) == "maquina/dispensar" && mensaje == "dispensar") {
        display.clearDisplay();
        display.setTextSize(1);
        display.setCursor(0, 25);
        display.println("Dispensando...");
        display.display();

        digitalWrite(LED_DISPENSAR, HIGH);
        delay(3000);
        digitalWrite(LED_DISPENSAR, LOW);

        display.clearDisplay();
        display.setCursor(0, 25);
        display.println("Listo!");
        display.display();
    }
}

void conectarMQTT() {
    while (!client.connected()) {
        Serial.println("Conectando al broker...");
        if (client.connect("ESP32Client")) {
            Serial.println("Conectado al broker!");
            client.subscribe("maquina/token");
            client.subscribe("maquina/dispensar");
        } else {
            Serial.print("Fallo, rc=");
            Serial.println(client.state());
            delay(5000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    delay(2000);

    // OLED
    Wire.begin(1, 2);
    if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        Serial.println("Error OLED");
        while(true);
    }

    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.println("Conectando WiFi...");
    display.display();

    // WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi conectado!");
    Serial.println(WiFi.localIP());

    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("WiFi OK!");
    display.println(WiFi.localIP().toString());
    display.display();
    delay(2000);

    pinMode(LED_DISPENSAR, OUTPUT);
    digitalWrite(LED_DISPENSAR, LOW);

    // Servo
    // servo.attach(PIN_SERVO);
    // servo.write(0);

    // MQTT
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);
    conectarMQTT();

    // pantalla de espera
    display.clearDisplay();
    display.setCursor(0, 20);
    display.println("Esperando...");
    display.display();
}

void loop() {
    if (!client.connected()) {
        conectarMQTT();
    }
    client.loop();
}