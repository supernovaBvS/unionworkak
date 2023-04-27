// Motor A
int ENA = 11; 
int IN1 = 10; 
int IN2 = 9;
// Motor B
int IN3 = 8; 
int IN4 = 7; 
int ENB = 6;

void setup() {
// put your setup code here, to run once: Serial.begin(9600);
pinMode(ENA, OUTPUT); 
pinMode(ENB, OUTPUT); 
pinMode(IN1, OUTPUT);
pinMode(IN2, OUTPUT);
pinMode(IN3, OUTPUT);
pinMode(IN4, OUTPUT);
}

void loop() { 
////////////////////////////////////////// 
// Set Motor A Direction 
digitalWrite(IN1, HIGH); 
digitalWrite(IN2, LOW);
// Enable Motor A - Use PWM for Speed 
//digitalWrite(ENA, LOW); 
analogWrite(ENA, 120); 
//////////////////////////////////////////
// Set Motor B Direction
digitalWrite(IN3, HIGH); 
digitalWrite(IN4, LOW);
// Enable Motor B - Use PWM for Speed 
//digitalWrite(ENB, HIGH); 
analogWrite(ENB, 200); 
////////////////////////////////////////////
}