#define LEDCHANNEL 0
#define FREQ 5000
#define RESOLUTION 12
#define LEDPIN 14
#define POTPIN 35

void setup(){
    Serial.begin(9600);
    ledcSetup(LEDCHANNEL,FREQ,RESOLUTION);
    ledcAttachPin(LEDPIN,LEDCHANNEL);
}
void loop(){
    Serial.println("Writing from Potentiometer.");
    int val = analogRead(POTPIN);
    ledcWrite(LEDCHANNEL,val);
}
/*
C POT-END1 -> ESP-GND
C POT-END2 -> ESP-3V3
C POT-DAT -> ESP-35
C LED-NEG -> ESP-GND
C LED-POS -> ESP-14
*/