#include <HCSR04.h>

int trigPin = 9;
int echoPin = 10;

HCSR04 hc(trigPin, echoPin);

void setup() {
  Serial.begin(9600); // Starts the serial communication
}
void loop() {
  Serial.println( hc.dist() );
  delay(60);
}