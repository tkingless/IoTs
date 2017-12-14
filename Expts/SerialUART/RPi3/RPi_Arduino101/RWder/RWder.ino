void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial1.begin(9600);
}

unsigned long lastMills = 0;
unsigned long interval = 2000;

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) { 
    // If anything comes in Serial (USB),
    char inputByte = Serial.read();
    Serial.println("Serial input then send to another board's Serial1, value: ");
    Serial.println(inputByte);
    Serial1.write(inputByte);   // read it and send it out Serial1 (pins 0 & 1)
  }

  if (Serial1.available()) {     // If anything comes in Serial1 (pins 0 & 1)
    char incomingByte = Serial1.read();
    Serial.print("external Serial1 get read then send to Serial, value: ");
    Serial.println(incomingByte);
    //Serial.write(incomingByte);   // read it and send it out Serial (USB)
  }

  if(millis() - lastMills >= interval){
      Serial1.write('L');
      lastMills = millis();
  }
}
