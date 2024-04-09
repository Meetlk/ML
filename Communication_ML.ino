Arduino Code for sensors and serial communication:

#include <SimpleDHT.h>
int pinDHT11 = 2;
SimpleDHT11 dht11(pinDHT11);
const int ldr_pin = A6;
const int wind_pin = A2;
void setup() {
  Serial.begin(115200);
  pinMode(ldr_pin, INPUT);
  pinMode(wind_pin, INPUT);
}
void loop(){
  int ldr = analogRead(ldr_pin);
  int wind = analogRead(wind_pin);
  int ldr_map = map(ldr, 100, 1000, 0, 10);
  int wind_map = map(wind, 0, 1023, 0, 57);
  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    return;
  }
  if(ldr_map<10)
  {
    Serial.print("0");
  }
  Serial.print(ldr_map);
  Serial.print((int)temperature); 
  Serial.print((int)humidity);
  if(wind_map<10)
  {
    Serial.print("0");
  }
  Serial.print(wind_map);
  delay(1500);
