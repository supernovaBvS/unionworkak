
int sensorPin = A0;
int sensorValue = 0;
int s1 = 378;
int s2 = 437;
int s3 = 530;
int s4 = 654;
int s5 = 823;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);
}

void loop() {
  button();
  // autton();
}

void autton() {

  sensorValue = analogRead(sensorPin);
  Serial.println(sensorValue);
  // delay(1000);
  if (sensorValue <= s1) {
    Serial.println("s1 is pressed");
    delay(1000);
  }
  else if (sensorValue <= s2){
    // Serial.println("s2 is pressed");
    delay(1000);
  }
  else if (sensorValue <440){
    // Serial.println("s3 is pressed");
    delay(1000);
  }
  else if (sensorValue <500){
    // Serial.println("s4 is pressed");
    delay(1000);
  }
  else if (sensorValue <600){
    // Serial.println("s5 is pressed");
    delay(1000);
  }
}

void button() {
  int buttonB = digitalRead(2);
  int buttonY = digitalRead(4);
  int buttonG = digitalRead(7);

  if (buttonB == 0) {
    Serial.println("Button B pressed");
    delay(100); // Add delay to prevent rapid button presses
  }
  if (buttonY == 0) {
    Serial.println("Button Y pressed");
    // isSuctionCupOn = !isSuctionCupOn;
    // bot.SetEndEffectorSuctionCup(isSuctionCupOn, false, NULL);
    delay(100); // Add delay to prevent rapid button presses
  }
  // if (buttonG == 0) {
  //   Serial.println("Button G pressed");
  //   delay(100); // Add delay to prevent rapid button presses
  // }
}

