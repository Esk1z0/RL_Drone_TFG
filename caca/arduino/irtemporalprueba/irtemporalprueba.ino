#include <IRremote.hpp>

#define IR_RECIEVE_PIN 11

void setup() {
  IrReceiver.begin(IR_RECIEVE_PIN);
  Serial.begin(9600);
}

void loop() {
  if (IrReceiver.decode()) {
    IrReceiver.resume();
    Serial.println(IrReceiver.decodedIRData.command);
  }
  delay(300);
}
