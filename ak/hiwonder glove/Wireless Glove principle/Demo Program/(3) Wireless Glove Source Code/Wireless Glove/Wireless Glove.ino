#include <SoftwareSerial.h>
#include "LobotServoController.h"

#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

#define BTH_RX 11
#define BTH_TX 12

// Define finger potentiometer pins
const int THUMB_PIN = A0;
const int INDEX_PIN = A1;
const int MIDDLE_PIN = A2;
const int RING_PIN = A3;
const int PINKY_PIN = A6;

float min_list[5] = {0, 0, 0, 0, 0};
float max_list[5] = {255, 255, 255, 255, 255};
float sampling[5] = {0, 0, 0, 0, 0};
float data[5] = {1500, 1500, 1500, 1500, 1500};
bool turn_on = true;
SoftwareSerial Bth(BTH_RX, BTH_TX);
LobotServoController lsc(Bth);

float float_map(float in, float left_in, float right_in, float left_out, float right_out)
{
  return (in - left_in) * (right_out - left_out) / (right_in - left_in) + left_out;
}

MPU6050 accelgyro;
int16_t ax, ay, az;
int16_t gx, gy, gz;
float ax0, ay0, az0;
float gx0, gy0, gz0;
float ax1, ay1, az1;
float gx1, gy1, gz1;

int ax_offset, ay_offset, az_offset, gx_offset, gy_offset, gz_offset;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //Initialize the function button
  pinMode(7, INPUT_PULLUP);
  // //Each finger potentiometer configuration
  // pinMode(A0, INPUT);
  // pinMode(A1, INPUT);
  // pinMode(A2, INPUT);
  // pinMode(A3, INPUT);
  // pinMode(A6, INPUT);
  // Initialize finger potentiometer pins
  pinMode(THUMB_PIN, INPUT);
  pinMode(INDEX_PIN, INPUT);
  pinMode(MIDDLE_PIN, INPUT);
  pinMode(RING_PIN, INPUT);
  pinMode(PINKY_PIN, INPUT);
  //LED configuration
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);

  //Bluetooth Configuration
  Bth.begin(9600);
  Bth.write("AT+CONN=BC:D0:74:2F:D3:F7\r\n");
  Bth.print("AT");
  Bth.print("AT+NAME=Gloves"); // Set BT name 
  Bth.print("AT+ROLE=S");  // Set Bluetooth Configuration main mode
  delay(100);
  Bth.print("AT+RESET");  //Soft reset Bluetooth module
  delay(250);

  //MPU6050 configuration
  Wire.begin();
  accelgyro.initialize();
  accelgyro.setFullScaleGyroRange(3); // Set angular velocity range
  accelgyro.setFullScaleAccelRange(1); //Set accelerated speed range
  delay(200);
  accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);  //Get current axis data to calibrate
  ax_offset = ax;  //X axis acceleration calibration data
  ay_offset = ay;  //Y axis acceleration calibration data
  az_offset = az - 8192;  //Z axis acceleration calibration data
  gx_offset = gx; //X-axis angular velocity calibration data
  gy_offset = gy; //Y-axis angular velocity calibration data
  gz_offset = gz; //Z-axis angular velocity calibration data
}



//Get individual finger potentiometer data
void finger() {
  // put your main code here, to run repeatedly:
  static uint32_t timer_sampling;
  static uint32_t timer_init;
  static uint32_t timer_lsc = 0;
  static uint8_t init_step = 0;
  if (timer_lsc == 0)
    timer_lsc = millis();
  if (timer_sampling <= millis())
  {
    for (int i = 14; i <= 18; i++)
    {
      if (i < 18)
        sampling[i - 14] += analogRead(i); //Read individual finger data
      else
        sampling[i - 14] += analogRead(A6);  // Read the little finger data, because the IIC uses A4, A5, so it cannot read continuously from A0
      sampling[i - 14] = sampling[i - 14] / 2.0; //Take the average of the previous and current measurements
      data[i - 14 ] = float_map( sampling[i - 14],min_list[i - 14], max_list[i - 14], 2500, 500); //Map the measurement to 500-2500, 500 for gripping and 2500 for opening
      data[i - 14] = data[i - 14] > 2500 ? 2500 : data[i - 14];  // The maximum limit is 2500
      data[i - 14] = data[i - 14] < 500 ? 500 : data[ i - 14];   //The minimum limit is 500
    }
    //timer_sampling = millis() + 10;
  }

  if (turn_on && timer_init < millis())
  {
    switch (init_step)
    {
      case 0:
        digitalWrite(2, LOW);
        digitalWrite(3, LOW);
        digitalWrite(4, LOW);
        digitalWrite(5, LOW);
        digitalWrite(6, LOW);
        timer_init = millis() + 20;
        init_step++;
        break;
      case 1:
        digitalWrite(2, HIGH);
        digitalWrite(3, HIGH);
        digitalWrite(4, HIGH);
        digitalWrite(5, HIGH);
        digitalWrite(6, HIGH);
        timer_init = millis() + 200;
        init_step++;
        break;
      case 2:
        digitalWrite(2, LOW);
        digitalWrite(3, LOW);
        digitalWrite(4, LOW);
        digitalWrite(5, LOW);
        digitalWrite(6, LOW);
        timer_init = millis() + 50;
        init_step++;
        break;
      case 3:
        digitalWrite(2, HIGH);
        digitalWrite(3, HIGH);
        digitalWrite(4, HIGH);
        digitalWrite(5, HIGH);
        digitalWrite(6, HIGH);
        timer_init = millis() + 500;
        init_step++;
        Serial.print("max_list:");
        for (int i = 14; i <= 18; i++)
        {
          max_list[i - 14] = sampling[i - 14];
          Serial.print(max_list[i - 14]);
          Serial.print("-");
        }
        Serial.println();
        break;
      case 4:
        init_step++;
        break;
      case 5:
        if ((max_list[1] - sampling[1]) > 50)
        {
          init_step++;
          digitalWrite(2, LOW);
          digitalWrite(3, LOW);
          digitalWrite(4, LOW);
          digitalWrite(5, LOW);
          digitalWrite(6, LOW);
          timer_init = millis() + 2000;
        }
        break;
      case 6:
        digitalWrite(2, HIGH);
        digitalWrite(3, HIGH);
        digitalWrite(4, HIGH);
        digitalWrite(5, HIGH);
        digitalWrite(6, HIGH);
        timer_init = millis() + 200;
        init_step++;
        break;
      case 7:
        digitalWrite(2, LOW);
        digitalWrite(3, LOW);
        digitalWrite(4, LOW);
        digitalWrite(5, LOW);
        digitalWrite(6, LOW);
        timer_init = millis() + 50;
        init_step++;
        break;
      case 8:
        digitalWrite(2, HIGH);
        digitalWrite(3, HIGH);
        digitalWrite(4, HIGH);
        digitalWrite(5, HIGH);
        digitalWrite(6, HIGH);
        timer_init = millis() + 500;
        init_step++;
        Serial.print("min_list:");
        for (int i = 14; i <= 18; i++)
        {
          min_list[i - 14] = sampling[i - 14];
          Serial.print(min_list[i - 14]);
          Serial.print("-");
        }
        Serial.println();
        lsc.runActionGroup(0, 1);
        turn_on = false;
        break;

      default:
        break;
    }
  }
}


float radianX;
float radianY;
float radianZ;
float radianX_last; //Finally get X axis inclination
float radianY_last; //Finally get Y axis inclination


//Update tilt sensor data
void update_mpu6050()
{
  static uint32_t timer_u;
  if (timer_u < millis())
  {
    // put your main code here, to run repeatedly:
    timer_u = millis() + 20;
    accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    ax0 = ((float)(ax)) * 0.3 + ax0 * 0.7;  //Filter the read value
    ay0 = ((float)(ay)) * 0.3 + ay0 * 0.7;
    az0 = ((float)(az)) * 0.3 + az0 * 0.7;
    ax1 = (ax0 - ax_offset) /  8192.0;  // Corrected and converted to multiples of gravitational acceleration
    ay1 = (ay0 - ay_offset) /  8192.0;
    az1 = (az0 - az_offset) /  8192.0;

    gx0 = ((float)(gx)) * 0.3 + gx0 * 0.7;  //Filter the value reading from the angular velocity
    gy0 = ((float)(gy)) * 0.3 + gy0 * 0.7;
    gz0 = ((float)(gz)) * 0.3 + gz0 * 0.7;
    gx1 = (gx0 - gx_offset);  //Correct angular velocity
    gy1 = (gy0 - gy_offset);
    gz1 = (gz0 - gz_offset);


    //Complementary calculation of x-axis inclination
    radianX = atan2(ay1, az1);
    radianX = radianX * 180.0 / 3.1415926;
    float radian_temp = (float)(gx1) / 16.4 * 0.02;
    radianX_last = 0.8 * (radianX_last + radian_temp) + (-radianX) * 0.2;

    //Complementary calculation of y-axis inclination
    radianY = atan2(ax1, az1);
    radianY = radianY * 180.0 / 3.1415926;
    radian_temp = (float)(gy1) / 16.4 * 0.01;
    radianY_last = 0.8 * (radianY_last + radian_temp) + (-radianY) * 0.2;
  }
}

//print data
void print_data()
{
  static uint32_t timer_p;
  static uint32_t timer_printlog;
  if ( 0&&timer_p < millis())
  {
    Serial.print("ax:"); Serial.print(ax1);
    Serial.print(", ay:"); Serial.print(ay1);
    Serial.print(", az:"); Serial.print(az1);
    Serial.print(", gx:"); Serial.print(gx1);
    Serial.print(", gy:"); Serial.print(gy1);
    Serial.print(", gz:"); Serial.print(gz1);
    Serial.print(", GX:"); Serial.print(radianX_last);
    Serial.print(", GY:"); Serial.println(radianY_last);
    timer_p = millis() + 500;
  }

  if (timer_printlog <= millis())  //To output data, remove 0 &&
  {
    for (int i = 14; i <= 18; i++)
    {
      Serial.print(data[i - 14]);
      Serial.print("  ");
      // Serial.print(float_map(min_list[i-14], max_list[i-14], 500,2500,sampling[i-14]));
      Serial.print(" ");
      // Serial.print();
    }
    timer_printlog = millis() + 1000;
    Serial.println();
  }
  // Read finger positions
  int thumb_pos = analogRead(THUMB_PIN);
  int index_pos = analogRead(INDEX_PIN);
  int middle_pos = analogRead(MIDDLE_PIN);
  int ring_pos = analogRead(RING_PIN);
  int pinky_pos = analogRead(PINKY_PIN);

  // Check if each finger is moving
  // if (radianY_last < -35 && radianY_last > -90 && middle_pos > 500  && ring_pos > 500) {
  //   Serial.println("turning right!");
  // }
  // if (radianY_last < 90 && radianY_last > 35 && middle_pos > 500  && ring_pos > 500)    //Right palm angle greater than 35 degrees and less than 90 degrees, middle finger outstretched ring finger to show bending
  // {
  //   Serial.println("turning left!");
  // }
  // if ((radianY_last < 15 &&  radianY_last > -15 ) && data[2] > 2100 && data[3] > 2100)  //With the palm facing down, open hands (middle finger straight), move forward
  // {
  //   Serial.println("STOP!");
  // }
  // if ((radianY_last < 15 && radianY_last > -15) && data[2] < 600)  //With the palm facing down, make a fist (the middle finger bends),then stop
  // {
  //   Serial.println("GO_FORWARD!");
  // }
  // if (thumb_pos > 500) {
  //   Serial.println("Thumb is moving!");
  // }
  // if (index_pos > 500) {
  //   Serial.println("Index finger is moving!");
  // }
  // if (middle_pos > 500) {
  //   Serial.println("Middle finger is moving!");
  // }
  // if (ring_pos > 500) {
  //   Serial.println("Ring finger is moving!");
  // }
  // if (pinky_pos > 500) {
  //   Serial.println("Pinky finger is moving!");
  // }
  // Delay for a short time to avoid spamming the serial monitor
  // delay(100);
}

#define STOP       0
#define GO_FORWARD 1
#define GO_BACK    2
#define TURN_LEFT  3
#define TURN_RIGHT 4

//run, control the Hexapod robot
void run()
{
  static uint32_t timer;
  static uint32_t step;
  static int act;
  static int last_act;
  if (timer > millis())
    return;
  timer = millis() + 80;
  if (radianY_last < -35 && radianY_last > -90 && data[3] < 1200  && data[2] > 2000) //Right palm angle greater than 35 degrees and less than 90 degrees, middle finger outstretched ring finger to show bending
  {
    act = TURN_RIGHT; // Turn to the right
  }
  if (radianY_last < 90 && radianY_last > 35 && data[3] < 1200 && data[2] > 2000)    //Right palm angle greater than 35 degrees and less than 90 degrees, middle finger outstretched ring finger to show bending
  {
    act = TURN_LEFT; //Turn to the left
  }
  if ((radianY_last < 15 && radianY_last > -15) && data[2] < 600)  //With the palm facing down, make a fist (the middle finger bends),then stop
  {
    act = STOP;
  }
  if ((radianY_last < 15 &&  radianY_last > -15 ) && data[2] > 2100 && data[3] > 2100)  //With the palm facing down, open hands (middle finger straight), move forward
  {
    act = GO_FORWARD;
  }
  if ((radianY_last < -130 ||  radianY_last > 130 ) && data[2] < 1200 && data[4] > 2000)  //With the palm facing up, the middle finger being bent, with the little finger being straightened (Spider-Man action),
  {
    act = GO_BACK;
  }
  if ((radianY_last < -130 ||  radianY_last > 130 ) && data[2] > 2000) //With the palm facing up, open hand than stop
  {
    act = STOP;
  }
  if (act != last_act)
  {
    last_act = act;
    if (act == STOP)
    {
      lsc.stopActionGroup();  //Stop current action groups
      lsc.runActionGroup(0, 1);  //Run specified action group
      //   Serial.println("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS");
      return;
    }
    if (act == GO_FORWARD)
    {
      lsc.stopActionGroup();
      lsc.runActionGroup(1, 0);
      //   Serial.println("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
      return;
    }
    if (act == GO_BACK)
    {
      lsc.stopActionGroup();
      lsc.runActionGroup(2, 0);
      //   Serial.println("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB");
      return;
    }
    if (act == TURN_LEFT)
    {
      lsc.stopActionGroup();
      lsc.runActionGroup(3, 0);
      return;
    }
    if (act == TURN_RIGHT)
    {
      lsc.stopActionGroup();
      lsc.runActionGroup(4, 0);
      return;
    }

  }
}

//run1, Control robotic hand。
void run1()
{
  if (data[1] < 1000 && data[2] < 1000 && data[3] < 1000)  //If the value of the finger less than a certain value, control the handshaking
  { 
    lsc.moveServos(5, 1000, 1, 1950, 2, 1100, 3, 1150, 4, 1160, 5, 1775);
    delay(1000);
  } else if (data[1] > 1400 && data[2] > 1400 && data[3] > 1400) //If the value of the finger larger than a certain value,control the palm being opened
  {
    lsc.moveServos(5, 1000, 1, 1050, 2, 1950, 3, 1900, 4, 1900, 5, 1050);
    delay(1000);
  }
}

//Send the digital value to the car
void car_control(byte act, byte sp)
{
  byte buf[10];
  buf[0] = buf[1] = 0x55;
  buf[2] = 0x04;
  buf[3] = 0x01;
  buf[4] = (byte)act;
  buf[5] = (byte)sp;
  Bth.write(buf, 6);
}
//run2,control the car
void run2()
{
  static uint32_t timer;
  static uint32_t step;
  int act = 0;
  static int last_act;
  if (timer > millis())
    return;
  timer = millis() + 100;
  if (radianY_last < -35 && radianY_last > -90 && data[3] < 1500  && data[2] > 1800)//Stretch the index finger and middle finger, hold the other fingers tightly, if the hand tilt right, then turn right
  {
    act = TURN_RIGHT;
  } else if (radianY_last < 90 && radianY_last > 35 && data[3] < 1500 && data[2] > 1800) //Stretch out the index finger and middle finger, hold the other fingers tightly,if the hand tilt right,then turn left
  {
    act = TURN_LEFT;
  } else if (radianY_last < 25 && radianY_last > -25 && data[3] < 1500 && data[2] > 1800 &&  radianX_last > 20) //With the palm facing down, stretch your index finger and middle finger, obliquely pointing up, the car move backward.
  {
    act = GO_BACK;
  } else if (radianY_last < 25 && radianY_last > -25 && data[3] < 1500 && data[2] > 1800 &&  radianX_last < -20) //With the palm facing down,the index finger and middle finger are extended,obliquely pointing down and the car stops.
  {
    act = GO_FORWARD;
  } else {
    act = STOP;
  }
  if (1)
  {
    last_act = act;
    if (act == STOP)
    {
      car_control(act, 0); // Control the car stop
      return;
    }
    if (act == GO_FORWARD)
    {
      car_control(act, 8); //Control the car move forward
      return;
    }
    if (act == GO_BACK)
    {
      car_control(act, 8);
      return;
    }
    if (act == TURN_LEFT)
    {
      car_control(act, 7);
      return;
    }
    if (act == TURN_RIGHT)
    {
      car_control(act, 7);
      return;
    }
  }
}

//run3, control the robotic arm
void run3()
{
  static uint32_t timer;
  static uint32_t step;
  int act = 0;
  static int last_act;
  if (timer > millis())
    return;
  timer = millis() + 50;
  //  float rl = radianY_last;
  //  float td = radianX_last;
  //  rl = rl < -60 ? -60 : rl;
  //  td = td < -60 ? -60 : td;
  //  rl = rl > 60 ? 60 : rl;
  //  td = td > 60 ? 60 : td;
  //  Serial.println(rl);
  //  rl = float_map(rl, -60, 60, 500, 2500);
  //  td = float_map(td, -60, 60, 2500, 500);
  //  Serial.println(rl);
  //  lsc.moveServo(6,(uint16_t)rl, 100);
  //  lsc.moveServo(5,(uint16_t)td, 100);
  //  lsc.moveServo(1,(uint16_
  if (radianY_last < -60) //The finger leans to the right, then performs a specified action group
  {
    lsc.runActionGroup(21, 1);
    lsc.waitForStopping(10000);
    return;
  }
  if (radianY_last > 30) //The finger leans to the left, then performs a specified action group
  {
    lsc.runActionGroup(22, 1);
    lsc.waitForStopping(10000); //Wait for the action group to complete, the timeout is 10000 milliseconds
    return;
  }
}
int mode = 0;
bool key_state = false;
void loop() {
  finger();  //Update the finger potentiometer data
  update_mpu6050();  //Update tilt sensor value

  if (turn_on == false) //After startup, potentiometer complete calibration.
  {
    if(key_state == true && digitalRead(7) == true)
    {
      delay(30);
      if(digitalRead(7) == true)
        key_state = false;
    }
    if (digitalRead(7) == false && key_state == false)
    {
      delay(30);
      if (digitalRead(7) == false)
      {
        key_state = true;
        if (mode == 3)
        {
          mode = 0;
        }
        else
          mode++;
        if (mode == 0)
        {
          digitalWrite(2, HIGH);
          digitalWrite(3, HIGH);
          digitalWrite(4, HIGH);
          digitalWrite(5, HIGH);
          digitalWrite(6, HIGH);
        }
        if (mode == 1)
        {
          digitalWrite(2, LOW);
          digitalWrite(3, HIGH);
          digitalWrite(4, HIGH);
          digitalWrite(5, HIGH);
          digitalWrite(6, HIGH);
        }
        if (mode == 2)
        {
          digitalWrite(2, LOW);
          digitalWrite(3, LOW);
          digitalWrite(4, HIGH);
          digitalWrite(5, HIGH);
          digitalWrite(6, HIGH);
        }
        if (mode == 3)
        {
          digitalWrite(2, LOW);
          digitalWrite(3, LOW);
          digitalWrite(4, LOW);
          digitalWrite(5, HIGH);
          digitalWrite(6, HIGH);
        }
      }
    }
    if (mode == 0)
      run();  // Spiderbot
    if (mode == 1)
   //   run1(); // Robotic palm
    if (mode == 2)
      run2(); // Robotic car
    if (mode == 3)
      run3();  //Robotic Arm
  }

  print_data();  //Print sensor data for easy debugging
}

