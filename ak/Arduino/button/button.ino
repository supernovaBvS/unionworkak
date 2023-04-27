void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);
}

void loop() {
  // put your main code here, to run repeatedly:
  int button1 = digitalRead(2);

    if (button1 == 0)//if variablebutton1 is 0
  {
    Serial.println("pressed");

  } else {
    Serial.println("not pressed");
  }
}
