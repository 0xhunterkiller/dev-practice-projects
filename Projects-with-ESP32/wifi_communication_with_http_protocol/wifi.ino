#include<WiFi.h>
#include<HTTPClient.h>

const char *ssid = "wifi_name";
const char *pwd = "wifi_password";

void setup(){
    WiFi.begin(ssid,pwd);
    Serial.begin(9600);
    Serial.print("Connected...");
    while(WiFi.status() != WL_CONNECTED){
        Serial.print(".");
        delay(500);
    }
    Serial.println("\nConnected");
}
void loop(){
    HTTPClient http;
    if(Wifi.status() == WL_CONNENCTED){
        http.begin("http://127.0.0.1/get-sensor?temperature=245");
        int httpCode = http.GET();
        if (httpCode > 0){
            String payload = http.getString();
            Serial.println(httpCode);
            Serial.println(payload);
        }
        else{
            Serial.println("Error in HTTP");
        }
    }
    else{
        delay(1000);
    }
    http.end();
}
