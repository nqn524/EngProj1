#include <ArduinoBLE.h>

BLEService dataService("180C");

BLEIntCharacteristic dataCharacteristic("2A56", BLERead | BLENotify);

int counter = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Start BLE
  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  // Set device name
  BLE.setLocalName("CUNT");
  BLE.setAdvertisedService(dataService);

  dataService.addCharacteristic(dataCharacteristic);

  BLE.addService(dataService);

  dataCharacteristic.writeValue(counter);

  BLE.advertise();

  Serial.println("BLE device is now advertising...");
}

void loop() {
  BLEDevice central = BLE.central();

  // If a device connects
  if (central) {
    Serial.print("Connected to: ");
    Serial.println(central.address());

    while (central.connected()) {
      counter++;

      dataCharacteristic.writeValue(counter);

      Serial.print("Sent: ");
      Serial.println(counter);

      delay(1000);
    }

    Serial.println("Disconnected");
  }
}
