#include <Wire.h>

// Constants:
const int flexPin1 = A0; // to read analog input from 1st flex sensor
const int flexPin2 = A1; // to read analog input from 2nd flex sensor
const int flexPin3 = A2; // to read analog input from 3rd flex sensor
const int flexPin4 = A3; // to read analog input from 4th flex sensor
const int flexPin5 = A4; // to read analog input from 5th flex sensor

// Variables:
int value1;
int value2;
int value3;
int value4;
int value5;

// Values from 3 contact sensors
int pinx = 12;
int piny = 8;
int pinz = 10;

// MPU-6050 variables
int xpin = A8; // x-axis of the accelerometer
int ypin = A9; // y-axis
int zpin = A10; // z-axis (only on 3-axis models)

int v1 = 0;
int v2 = 0;
int v3 = 0;
int v4 = 0;
int v5 = 0;
int v6 = 0;
int v7 = 0;
int v8 = 0;
int v9 = 0;

void setup() {
  Serial.begin(9600);
  pinMode(pinx, INPUT);
  digitalWrite(pinx, HIGH);
  pinMode(piny, INPUT);
  digitalWrite(piny, HIGH);
  pinMode(pinz, INPUT);
  digitalWrite(pinz, HIGH);

  // Initiate communication with MPU-6050
  Wire.begin();

  Serial.println("CLEARDATA");
  Serial.print("LABEL,F1,F2,F3,F4,F5,X,Y,Z,C1,C2,GX,GY,GZ");
  Serial.println();
}

void loop() {
  // Read values from flex sensors
  value1 = analogRead(flexPin1);
  value2 = analogRead(flexPin2);
  value3 = analogRead(flexPin3);
  value4 = analogRead(flexPin4);
  value5 = analogRead(flexPin5);

  // Read values from MPU-6050 accelerometer
  Wire.beginTransmission(0x68); // Address of MPU-6050
  Wire.write(0x3B); // Starting register for accelerometer data
  Wire.endTransmission(false);
  Wire.requestFrom(0x68, 14, true); // Request 14 bytes of data

  int16_t AcX = Wire.read() << 8 | Wire.read();
  int16_t AcY = Wire.read() << 8 | Wire.read();
  int16_t AcZ = Wire.read() << 8 | Wire.read();

  // Read values from MPU-6050 gyroscope
  Wire.beginTransmission(0x68); // Address of MPU-6050
  Wire.write(0x43); // Starting register for gyroscope data
  Wire.endTransmission(false);
  Wire.requestFrom(0x68, 14, true); // Request 14 bytes of data

  int16_t GyX = Wire.read() << 8 | Wire.read();
  int16_t GyY = Wire.read() << 8 | Wire.read();
  int16_t GyZ = Wire.read() << 8 | Wire.read();

  // Map accelerometer values to 0-255
  v2 = map(AcX, -32768, 32767, 0, 255);
  v4 = map(AcY, -32768, 32767, 0, 255);
  v6 = map(AcZ, -32768, 32767, 0, 255);

  // Map gyroscope values to 0-255
  v7 = map(GyX, -32768, 32767, 0, 255);
  v8 = map(GyY, -32768, 32767, 0, 255);
  v9 = map(GyZ, -32768, 32767, 0, 255);

  // Read digital values from contact sensors
  v1 = digitalRead(pinx);
  v3 = digitalRead(piny);
  v5 = digitalRead(pinz);

  // Print values
  Serial.print("DATA,TIME,");
  Serial.print(value1);
  Serial.print(",");
  Serial.print(value2);
  Serial.print(",");
  Serial.print(value3);
  Serial.print(",");
  Serial.print(value4);
  Serial.print(",");
  Serial.print(value5);
  Serial.print(",");
  Serial.print(v2);
  Serial.print(",");
  Serial.print(v4);
  Serial.print(",");
  Serial.print(v6);
  Serial.print(",");
  Serial.print(v1);
  Serial.print(",");
  Serial.print(v3);
  Serial.print(",");
  Serial.print(v5);
  Serial.print(",");
  Serial.print(v7);
  Serial.print(",");
  Serial.print(v8);
  Serial.print(",");
  Serial.print(v9);
  Serial.println();

  // Delay before next reading
  delay(500);
}