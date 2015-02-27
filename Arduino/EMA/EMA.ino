#include <SFE_BMP180.h>
#include "DHT.h"
#include <Wire.h>

#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

SFE_BMP180 pressure;
#define ALTITUDE 16.0

void setup() {
    Serial.begin(9600);

    if (!pressure.begin())
      while(1) {
            Serial.println("fail");
      }
}

void loop() {
    char status;
    double T,P,H; // T en C, P en %, H en mBar
    delay(2000);
    
    H = dht.readHumidity();
    T = dht.readTemperature();
    
    status = pressure.startPressure(3);
    if (status != 0) {
      delay(status);
      status = pressure.getPressure(P, T);
    }
    
    Serial.print(T);
    Serial.print(",");
    Serial.print(H);
    Serial.print(",");
    Serial.println(P);
}
