## Template
```c
// declaration
void setup() {
	// Pin Setup, Serial.begin(), ledcAttachPin(), etc.
}
void loop() {
	// Whatever is given here runs infinitely.
}
```

## Pins
### setup
* pinMode(int pinNum, INPUT) // for Sensors (Input)
* pinMode(int pinNum, OUTPUT) // for Actuators (Output)
### loop
* digitalWrite(int pinNum, LOW) // Write a digital zero to the actuator component
* digitalWrite(int pinNum, HIGH) // Write a digital one to the actuator component
* int val = analogRead(int pinNum) // Read from a analong GPIO Pin (No INPUT Declaration required for such pins)














