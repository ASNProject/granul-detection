int sensor = A0;
unsigned long timerStart = 0;  
bool isCounting = false;      

void setup() {
  Serial.begin(115200);
  pinMode(sensor, INPUT);
}

void loop() {
  int result = analogRead(sensor); 
  unsigned long currentMillis = millis();

  if (result <= 10) {
    if (!isCounting) {
      timerStart = currentMillis;
      isCounting = true;
    }
  } else {
    if (isCounting) {
      unsigned long elapsedTime = currentMillis - timerStart;
      Serial.println(elapsedTime / 1000.0, 2);
      isCounting = false;
    }
  }

  // Hapus comment jika ingin menampilkan hasil kiriman dari python
//   if (Serial.available() > 0) {
//     String data = Serial.readString();
//     Serial.print(";");
//     Serial.println(data);
//   }

  delay(100);
}
