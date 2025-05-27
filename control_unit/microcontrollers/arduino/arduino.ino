// gate_esp32.ino
#include <esp_now.h>
#include <WiFi.h>

#define RELAY_PIN 5 // GPIO5 or any pin for relay control
unsigned long lastSeen = 0;
bool gateOpen = false;

typedef struct struct_message {
  bool carIsNear;
} struct_message;

struct_message incomingData;

void onReceive(const esp_now_recv_info_t *info, const uint8_t *incomingData, int len) {
  char macStr[18];
  snprintf(macStr, sizeof(macStr),
           "%02X:%02X:%02X:%02X:%02X:%02X",
           info->src_addr[0], info->src_addr[1], info->src_addr[2],
           info->src_addr[3], info->src_addr[4], info->src_addr[5]);

  Serial.print("Message received from: ");
  Serial.println(macStr);

  // Cast incomingData if you're expecting a struct
  // Example:
  // memcpy(&myStruct, incomingData, sizeof(myStruct));
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW); // gate closed initially

  esp_now_init();
  esp_now_register_recv_cb(onReceive);
}

void loop() {
  // If more than 10s passed without car, close gate
  if (gateOpen && millis() - lastSeen > 10000) {
    closeGate();
  }
}

void openGate() {
  Serial.println("Opening gate...");
  digitalWrite(RELAY_PIN, HIGH); // turn on relay to open
  gateOpen = true;
}

void closeGate() {
  Serial.println("Closing gate...");
  digitalWrite(RELAY_PIN, LOW); // turn off relay to close
  gateOpen = false;
}
