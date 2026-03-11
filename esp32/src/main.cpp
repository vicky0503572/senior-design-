#include <Arduino.h>
#include <ArduinoJson.h>
#include <Adafruit_BMP085.h>
#include <Adafruit_SHT31.h>
#include "HardwareSerial.h"

// LoRa UART
#define LORA_RX 16
#define LORA_TX 17
HardwareSerial LoRaSerial(2);   // UART2

const int LORA_NETWORK_ID = 5;
const int LORA_ADDRESS = 1;       // this ESP32 / weather box
const int LORA_DESTINATION = 2;   // gateway

Adafruit_BMP085 bmp;     
Adafruit_SHT31 sht3x = Adafruit_SHT31();

// helper: celcius -> farenheit
float cToF(float c) {
  return (c * 9.0 / 5.0) + 32.0;
}

void sendATCommand(const String &cmd, int waitMs = 500) {
  LoRaSerial.println(cmd);
  delay(waitMs);

  while (LoRaSerial.available()) {
    Serial.write(LoRaSerial.read());
  }
}

void setupLoRa() {
  Serial.println("Configuring LoRa module...");

  sendATCommand("AT", 300);
  sendATCommand("AT+RESET", 1000);
  sendATCommand("AT+NETWORKID=" + String(LORA_NETWORK_ID), 500);
  sendATCommand("AT+ADDRESS=" + String(LORA_ADDRESS), 500);
  sendATCommand("AT+PARAMETER?", 500);

  Serial.println("LoRa module configured.\n");
}

void sendLoRaMessage(const String &message) {
  String command = "AT+SEND=" + String(LORA_DESTINATION) + "," +
                   String(message.length()) + "," + message;

  LoRaSerial.println(command);

  Serial.println("Sending via LoRa:");
  Serial.println(message);

  delay(800);
  while (LoRaSerial.available()) {
    Serial.write(LoRaSerial.read());
  }
  Serial.println();
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("ESP32 Weather Box - Actual Data");

  // Start LoRa UART
  LoRaSerial.begin(115200, SERIAL_8N1, LORA_RX, LORA_TX);
  delay(1000);

  if (!bmp.begin()) {
    Serial.println("Could not find a valid BMP180/BMP085 sensor, check wiring!");
    while (1) { delay(10); }
  }

  if (!sht3x.begin(0x44)) {
    Serial.println("Could not find SHT30");
    while (1) { delay(10); }
  }

  setupLoRa();
}

void loop() {
  // Read BMP180
  float bmpTempC = bmp.readTemperature();
  float bmpTempF = cToF(bmpTempC);
  float pressurePa = bmp.readPressure();
  float pressurehPa = pressurePa / 100.0;

  // Read SHT30
  float shtTempC = sht3x.readTemperature();
  float shtHumidity = sht3x.readHumidity();

  // Check if SHT30 failed
  if (isnan(shtTempC) || isnan(shtHumidity)) {
    Serial.println("Failed to read from SHT30 sensor!");
    delay(2000);
    return;
  }

  float shtTempF = cToF(shtTempC);

  float temperatureF = shtTempF;

  // Print to Serial
  Serial.println("------ Sensor Reading ------");
  Serial.printf("SHT30 Temperature: %.1f°F (%.1f°C)\n", shtTempF, shtTempC);
  Serial.printf("SHT30 Humidity: %.1f%%\n", shtHumidity);
  Serial.printf("Pressure: %.1f hPa (%.0f Pa)\n", pressurehPa, pressurePa);
  Serial.printf("BMP Temp: %.1f°F (for reference)\n", bmpTempF);

  // Build JSON payload
  StaticJsonDocument<256> doc;
  doc["temperature_f"] = round(shtTempF * 10) / 10.0;   // Fahrenheit
  doc["temperature_c"] = round(shtTempC * 10) / 10.0;   // Celcius
  doc["humidity"] = round(shtHumidity * 10) / 10.0;
  doc["pressure"] = round(pressurehPa * 10) / 10.0;       // hPa
  doc["wind_speed"] = 0.0;      // TODO: waiting for wind sensor and rain sensor
  doc["wind_direction"] = 0;
  doc["rainfall"] = 0.0;

  String jsonString;
  serializeJson(doc, jsonString);

  // Send over LoRa
  sendLoRaMessage(jsonString);

  Serial.println("----------------------------\n");
  delay(5000); // every 5 seconds
}