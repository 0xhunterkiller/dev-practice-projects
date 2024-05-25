#include<dht.h>
#define DHTTYPE DHT11
#define DHTPIN 14
DHT dht(DHTPIN,DHTTYPE);
void setup() {
  // put your setup code here, to run once:
  dht.begin()
  Serial.begin(9600)
}

void loop() {
  // put your main code here, to run repeatedly:
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if(isnan(h) || isnan(t)){
    Serial.println("ERROR READING PARAMETERS FROM DHT");
  }
}
