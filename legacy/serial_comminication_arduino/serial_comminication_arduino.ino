const int buttonPin = 0;
int buttonState = 0;

unsigned long startTime = 0;
const unsigned long duration = 5000;
bool isTimerRunning = false;

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP);
}

void loop() {
  buttonState = digitalRead(buttonPin);

  if (buttonState == LOW && !isTimerRunning ) {
    startTime = millis();
    isTimerRunning = true;
    Serial.println("timer-0");
  } 

  if (isTimerRunning && (millis() - startTime >= duration)) {
    Serial.println("timer-" + String(duration));
    isTimerRunning = false;     // Reset flag timer
  }
  delay(50);
}