#define IRPIN 13
#define LEDPIN 2

void setup(){
    Serial.begin(9600);
    pinMode(IRPIN,INPUT);
    pinMode(LEDPIN,OUTPUT);
}
void loop(){
    if(digitalRead(IRPIN) == 0){
        Serial.println("Object Detected!");
        digitalWrite(LEDPIN,HIGH);
    }
    else{
        Serial.println("No Object Detected!");
        digitalWrite(LEDPIN,LOW);
    }
}

/*

CONNECT IR-GND TO ESP-GND
CONNECT LED-NEG TO ESP-GND
CONNECT LED-POS TO ESP-2
CONNECT IR-VCC TO ESP-VCC
CONNECT IR-DAT TO ESP-13

*/