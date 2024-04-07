int dcMotorPin = 3;

void setup() {
  pinMode(dcMotorPin, OUTPUT);
}

void loop() {
  for (int i=0; i<=224; i++){
    analogWrite(dcMotorPin, i);
    delay(50);
  }
  for (int i=224; i>0; i--){
    analogWrite(dcMotorPin, i);
    delay(50);
  }
}
