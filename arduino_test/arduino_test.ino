#include <Wire.h>
#include <TMRpcm.h>
#include <SD.h>
#include <SPI.h>

const int flexPin0 = A0;
const int flexPin1 = A1;
const int flexPin2 = A2;
const int microphonePin = A3;

int value0;
int value1;
int value2;
int microphoneValue;

const int chipSelect = 10;

const int MPU_ADDR = 0x68;
int16_t gyro_x, gyro_y, gyro_z;

const int speakerPin = 9;
TMRpcm tmrpcm;

unsigned long startTime = 0;
unsigned int duration = 2000;

char tmp_str[7];

char *convert_int16_to_str(int16_t i) {
  sprintf(tmp_str, "%6d", i);
  return tmp_str;
}

void playMP3(String command) {
  String filename = command + ".wav";

  if (SD.exists(filename)) {
    tmrpcm.play(filename.c_str());
  }
}

void setup() {
  Serial.begin(115200);

  tmrpcm.speakerPin = speakerPin;
  tmrpcm.setVolume(5);

  Wire.begin();
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);

  if (!SD.begin(10)) {
    return;
  }
}

void loop() {
  if (Serial.available() > 0) {
    String receivedString = Serial.readStringUntil('\n');
    // Riproduci MP3 corrispondente alla stringa ricevuta
    playMP3(receivedString);
    // Memorizza il tempo di inizio della riproduzione
    startTime = millis();

    delay(1000);
  }
  
  if (tmrpcm.isPlaying() && (millis() - startTime >= duration)) {
    tmrpcm.stopPlayback();
  }

  Serial.flush();

  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 7 * 2, true);

  gyro_x = Wire.read() << 8 | Wire.read();
  gyro_y = Wire.read() << 8 | Wire.read();
  gyro_z = Wire.read() << 8 | Wire.read();

  value0 = analogRead(flexPin0);
  value1 = analogRead(flexPin1);
  value2 = analogRead(flexPin2);

  microphoneValue = analogRead(microphonePin);

  Serial.print(value0);
  Serial.print(",");
  Serial.print(value1);
  Serial.print(",");
  Serial.print(value2);
  Serial.print(",");
  Serial.print(convert_int16_to_str(gyro_x));
  Serial.print(",");
  Serial.print(convert_int16_to_str(gyro_y));
  Serial.print(",");
  Serial.print(convert_int16_to_str(gyro_z));
  Serial.print(",");
  Serial.print(microphoneValue);
  Serial.println();

  delay(500);
}
