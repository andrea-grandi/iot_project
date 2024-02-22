#include <TinyGPS++.h>

#define GPS_BAUDRATE 9600  // Il baudrate predefinito del NEO-6M è 9600

TinyGPSPlus gps;  // L'oggetto TinyGPS++

void setup() {
  Serial.begin(9600);
  Serial2.begin(GPS_BAUDRATE);
}

void loop() {
  if (Serial2.available() > 0) {
    if (gps.encode(Serial2.read())) {
      if (gps.location.isValid()) {
        // Invia la latitudine, la longitudine e l'altitudine separatamente da una virgola
        Serial.print(gps.location.lat(), 6);  // Invia la latitudine con 6 cifre decimali
        Serial.print(",");
        Serial.print(gps.location.lng(), 6);  // Invia la longitudine con 6 cifre decimali
        Serial.print(",");
        if (gps.altitude.isValid())
          Serial.print(gps.altitude.meters(), 2);  // Invia l'altitudine con 2 cifre decimali
        else
          Serial.print("INVALID");

        Serial.print(",");
      } else {
        Serial.print("INVALID,INVALID,INVALID,");  // Se la posizione non è valida, invia "INVALID" per latitudine, longitudine e altitudine
      }

      // Invia la velocità
      if (gps.speed.isValid()) {
        Serial.print(gps.speed.kmph(), 2);  // Invia la velocità in km/h con 2 cifre decimali
      } else {
        Serial.print("INVALID");
      }

      Serial.print(",");

      // Invia la data e l'ora del GPS
      if (gps.date.isValid() && gps.time.isValid()) {
        Serial.print(gps.date.year());
        Serial.print("-");
        Serial.print(gps.date.month());
        Serial.print("-");
        Serial.print(gps.date.day());
        Serial.print(" ");
        Serial.print(gps.time.hour());
        Serial.print(":");
        Serial.print(gps.time.minute());
        Serial.print(":");
        Serial.print(gps.time.second());
      } else {
        Serial.print("INVALID");
      }

      Serial.println();  // Invia un carattere di nuova riga alla fine di ogni riga di dati
      delay(1000);
    }
  }

  if (millis() > 5000 && gps.charsProcessed() < 10)
    Serial.println(F("No GPS data received: check wiring"));
}