#define lmPin 35
#define adcVREF 3300
#define adcRES 4096
void setup(){
    Serial.begin(9600);
}
void loop(){
    int val = analogRead(lmPin);
    float mv = val*(adcVREF/adcRES);
    float tempC = mv/10;
    float tempF = (9/5)*tempC + 32;
    Serial.print("Temperature in Celsius is ");
    Serial.print(tempC);
    Serial.println(" degC");
    Serial.print("Temperature in Farenheit is ");
    Serial.print(tempF);
    Serial.println(" degF");
}

/*
C LM35-DAT -> ESP-35
C ESP-GND -> LM35-GND
C ESP-VIN -> LM35-VCC
*/