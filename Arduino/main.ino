#include <ArduinoBLE.h>
#include <math.h> // need for truncating
#include "Arduino_BMI270_BMM150.h" // the main library

BLEService dataService("180C");
BLEStringCharacteristic sendChat("2A56", BLERead | BLENotify, 96);
BLEStringCharacteristic receChat("2A57", BLEWrite, 50);

const bool PRINT = false;
const int FREQ = 24;

uint64_t PublicKeyN = 1;
uint64_t PublicKeyE = 1;

bool record = true;

struct pseudoArray
{
  float x;
  float y;
  float z;
  bool newData;
};

void setup() {
  if (PRINT) {
    Serial.begin(9600);
    while (!Serial);
  }

  SetupBLE();
  IMU.begin();
}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    bool keyRecieved = false;

    println("Connected to: " + central.address());
    println("Not subscribed");

    while (central.connected()) {
      if (sendChat.subscribed()) {
        if (keyRecieved) {
          pseudoArray accelData = IMUreader();

          if (accelData.newData & record) {
            //println("Raw: " + String(accelData.x) + " " + String(accelData.y) + " " + String(accelData.z));

            int time = millis();

            char buffer[96];
            sprintf(
              buffer,
              "%llu,%llu,%llu,%llu",
              (unsigned long long)Encrypt(accelData.x, PublicKeyE, PublicKeyN),
              (unsigned long long)Encrypt(accelData.y, PublicKeyE, PublicKeyN),
              (unsigned long long)Encrypt(accelData.z, PublicKeyE, PublicKeyN),
              (unsigned long long)Encrypt(time, PublicKeyE, PublicKeyN)
            );

            String sentData = String(buffer);
            //sentData = String(int(accelData.x)) + "," + String(int(accelData.y)) + "," + String(int(accelData.z)) + "," + String(millis());

            sendChat.writeValue(sentData);

            println("Raw: " + String((accelData.x - 5000000) / 100.0) + "," + String((accelData.y - 5000000) / 100.0) + "," + String((accelData.z - 5000000) / 100.0) + "," + String(time) + "    Encrypted: " + sentData);
          }

          if (receChat.written()) {
            String raw = receChat.value();

            if (raw == "start") {
              record = true;
            }

            if (raw == "stop") {
              record = false;
            }
          }
          delay(1000 / FREQ);
        }
        else {
          if (receChat.written()) {
            String raw = receChat.value();
            int length = receChat.valueLength();

            String KeyN = "";
            String KeyE = "";
            
            bool split = false;

            for (int i = 0; i < length; i++) {
                
              if (raw.substring(i,i+1) == ",") {
                split = true;
                continue;
              }
              else {
                if (!split) {
                  KeyN += (char)raw[i];
                }
                else {
                  KeyE += (char)raw[i];
                }
              }
            }

            PublicKeyN = strtoull(KeyN.c_str(), NULL, 10);
            PublicKeyE = strtoull(KeyE.c_str(), NULL, 10);

            keyRecieved = true;
            
            char buffer[64];
            sprintf(
              buffer,
              "%llu, %llu",
              (unsigned long long)PublicKeyN,
              (unsigned long long)PublicKeyE
            );
            println(buffer);
          }
          else {
            sendChat.writeValue("GIVEKEY");
            delay(1000);
          }
        }
      }
    }

    println("Disconnected");
  }
}

void println(String data) {
  if (PRINT) {
    if (Serial) {
      Serial.println(data);
    }
  }
}

void SetupBLE() {
  if (!BLE.begin()) {
    println("Starting BLE failed!");
    while (1);
  }

  BLE.setLocalName("CUNT");
  BLE.setAdvertisedService(dataService);

  dataService.addCharacteristic(sendChat);
  dataService.addCharacteristic(receChat);

  BLE.addService(dataService);

  sendChat.writeValue("ready");

  BLE.advertise();

  println("BLE device is now advertising...");
}

pseudoArray IMUreader() 
{
  pseudoArray position;
  position.newData = false;
  if (IMU.accelerationAvailable()) 
  {
    IMU.readAcceleration(position.x, position.y, position.z); // getting the data
    position.newData = true;
  }

  position.x = trunc((position.x*100) + 5000000); // editing the value to correct parameters
  position.y = trunc((position.y*100) + 5000000);
  position.z = trunc((position.z*100) + 5000000);
  if (position.x < 0)
  {
    position.x = 0;
  }
    if (position.y < 0)
  {
    position.y = 0;
  }
    if (position.z < 0)
  {
    position.z = 0;
  }

  return position;

}

uint64_t Encrypt(uint64_t PlainText, uint64_t PublicKeyE, uint64_t PublicKeyN) {
  uint64_t CipherText = 1;

  PlainText %= PublicKeyN;

  while (PublicKeyE > 0) {
    if (PublicKeyE & 1) {
      CipherText = mulmod(CipherText, PlainText, PublicKeyN);
    }
    PlainText = mulmod(PlainText, PlainText, PublicKeyN);
    PublicKeyE >>= 1;
  }

  return CipherText;
}

uint64_t mulmod(uint64_t a, uint64_t b, uint64_t mod) {
  uint64_t result = 0;
  a %= mod;

  while (b > 0) {
    if (b & 1) {
      result = (result + a) % mod;
    }
    a = (a << 1) % mod;
    b >>= 1;
  }

  return result;
}

