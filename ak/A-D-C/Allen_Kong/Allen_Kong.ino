
/****************************************Copyright(c)*****************************************************
**                            Shenzhen Yuejiang Technology Co., LTD.
**
**                                 http://www.dobot.cc
**
**--------------File Info---------------------------------------------------------------------------------
** File name:           main.cpp
** Latest modified Date:2016-10-24
** Latest Version:      V2.0.0
** Descriptions:        main body
**
**--------------------------------------------------------------------------------------------------------
** Modify by:           Edward
** Modified date:       2016-11-25
** Version:             V1.0.0
** Descriptions:        Modified,From DobotDemoForSTM32
**--------------------------------------------------------------------------------------------------------
*********************************************************************************************************/
#include "stdio.h"
#include "Protocol.h"
#include "command.h"
#include "FlexiTimer2.h"
//ak
// #include "Keyboard.h"
#include "dobotMag.h"
dobotMag bot(true);

//Set Serial TX&RX Buffer Size
#define SERIAL_TX_BUFFER_SIZE 64
#define SERIAL_RX_BUFFER_SIZE 256

// #define JOG_STICK
/*********************************************************************************************************
** Global parameters
*********************************************************************************************************/
EndEffectorParams gEndEffectorParams;

JOGJointParams  gJOGJointParams;
JOGCoordinateParams gJOGCoordinateParams;
JOGCommonParams gJOGCommonParams;
JOGCmd          gJOGCmd;

PTPCoordinateParams gPTPCoordinateParams;
PTPCommonParams gPTPCommonParams;
PTPCmd          gPTPCmd;

uint64_t gQueuedCmdIndex;
bool suspausta = false;

//ak
float startPosX = 250;       
float startPosY = 0;      
float startPosZ = 70;       
float startPosR = 0;       //Start position when powering up


////////////////// DABARTINES KORDINATES ///////////////////////////////
float currentX = 0;     
float currentY = 0;   
float currentZ = 0;   
float currentR = 0;
bool currentVac = false;
bool endeffectorGripper = true; // indicate type of end effector: true for gripper, false for vacuum cup

float currentjoint1 = 0;     
float currentjoint2 = 0;   
float currentjoint3 = 0;   
float currentjoint4 = 0;

/////////////////////////////////////////////////////////////////////////

/*********************************************************************************************************
** Function name:       setup
** Descriptions:        Initializes Serial
** Input parameters:    none
** Output parameters:   none
** Returned value:      none
*********************************************************************************************************/
//ak
#define led1 49
#define led2 48
#define led3 11
#define led4 43
#define led5 2

#define led6G 48
#define led7R 49
#define led8Y 7 
#define led9B 8

int previousButtonState = HIGH; 

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);
  
  printf_begin();
  //Set Timer Interrupt
  FlexiTimer2::set(100, Serialread);
  FlexiTimer2::start();
  Serial.println("Atnaujinta 2023-03-28 14:21");

  //ak
  pinMode(4, INPUT_PULLUP); //Y
  pinMode(42, INPUT_PULLUP);
  pinMode(51, INPUT_PULLUP);
  pinMode(50, INPUT_PULLUP);
  pinMode(13, INPUT_PULLUP);

  pinMode(4, INPUT_PULLUP); //Y
  pinMode(50, INPUT_PULLUP); //R
  pinMode(51, INPUT_PULLUP); //G
  pinMode(10, INPUT_PULLUP); //B
  pinMode(13, INPUT_PULLUP); //W
  
  pinMode(led,OUTPUT);

  //ak
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(led4, OUTPUT);
  pinMode(led5, OUTPUT);

  pinMode(led6G, OUTPUT);
  pinMode(led7R, OUTPUT);
  pinMode(led8Y, OUTPUT);
  pinMode(led9B, OUTPUT);
    
  // Setting the sensorOut as an input
  
  // Setting frequency scaling to 20%
  //ak
  digitalWrite(led1,HIGH);
  digitalWrite(led2,HIGH);
  digitalWrite(led3,HIGH);
  digitalWrite(led4,HIGH);
  digitalWrite(led5,HIGH);

  digitalWrite(led6G,HIGH);
  digitalWrite(led7R,HIGH);
  digitalWrite(led8Y,HIGH);
  digitalWrite(led9B,HIGH);
  // Begins serial communication 
  InitRAM();

  ProtocolInit();

  SetJOGJointParams(&gJOGJointParams, true, &gQueuedCmdIndex);

  SetJOGCoordinateParams(&gJOGCoordinateParams, true, &gQueuedCmdIndex);

  SetJOGCommonParams(&gJOGCommonParams, true, &gQueuedCmdIndex);
//ak
  printf("\r\n======Main Program loop started======\r\n");
  bot.setHomeParams(250,0,70,0); // set home position, default 250,0,50,0
  clear();
  // bot.setHome();
  
}

/*********************************************************************************************************
** Function name:       Serialread
** Descriptions:        import data to rxbuffer
** Input parametersnone:
** Output parameters:
** Returned value:
*********************************************************************************************************/
void Serialread()
{
  while (Serial1.available()) {
    uint8_t data = Serial1.read();
    if (RingBufferIsFull(&gSerialProtocolHandler.rxRawByteQueue) == false) {
      RingBufferEnqueue(&gSerialProtocolHandler.rxRawByteQueue, &data);
    }
  }
}
/*********************************************************************************************************
** Function name:       Serial_putc
** Descriptions:        Remap Serial to Printf
** Input parametersnone:
** Output parameters:
** Returned value:
*********************************************************************************************************/
int Serial_putc( char c, struct __file * )
{
  Serial.write( c );
  return c;
}

/*********************************************************************************************************
** Function name:       printf_begin
** Descriptions:        Initializes Printf
** Input parameters:
** Output parameters:
** Returned value:
*********************************************************************************************************/
void printf_begin(void){
  fdevopen( &Serial_putc, 0 );
}

/*********************************************************************************************************
** Function name:       InitRAM
** Descriptions:        Initializes a global variable
** Input parameters:    none
** Output parameters:   none
** Returned value:      none
*********************************************************************************************************/
void InitRAM(void)
{
    //Set JOG Model
    gJOGJointParams.velocity[0] = 100;
    gJOGJointParams.velocity[1] = 100;
    gJOGJointParams.velocity[2] = 100;
    gJOGJointParams.velocity[3] = 100;
    gJOGJointParams.acceleration[0] = 80;
    gJOGJointParams.acceleration[1] = 80;
    gJOGJointParams.acceleration[2] = 80;
    gJOGJointParams.acceleration[3] = 80;

    gJOGCoordinateParams.velocity[0] = 100;
    gJOGCoordinateParams.velocity[1] = 100;
    gJOGCoordinateParams.velocity[2] = 100;
    gJOGCoordinateParams.velocity[3] = 100;
    gJOGCoordinateParams.acceleration[0] = 80;
    gJOGCoordinateParams.acceleration[1] = 80;
    gJOGCoordinateParams.acceleration[2] = 80;
    gJOGCoordinateParams.acceleration[3] = 80;

    gJOGCommonParams.velocityRatio = 90;
    gJOGCommonParams.accelerationRatio = 90;
   
    gJOGCmd.cmd = AP_DOWN;
    gJOGCmd.isJoint = JOINT_MODEL;

    //Set PTP Model
    gPTPCoordinateParams.xyzVelocity = 100;
    gPTPCoordinateParams.rVelocity = 100;
    gPTPCoordinateParams.xyzAcceleration = 100;
    gPTPCoordinateParams.rAcceleration = 100;

    gPTPCommonParams.velocityRatio = 90;
    gPTPCommonParams.accelerationRatio = 90;

    gPTPCmd.ptpMode = JUMP_XYZ;
    
    gQueuedCmdIndex = 0;
    moveArm(startPosX, startPosY, startPosZ, startPosR);
    //moveranka(startPosX, startPosY, startPosZ, startPosR, true);
}
/*********************************************************************************************************
** Function name:       loop
** Descriptions:        Program entry
** Input parameters:    none
** Output parameters:   none
** Returned value:      none
*********************************************************************************************************/

//ak
bool end = false;
bool s = false;

void moveArm(double x, double y, double z, double r)
{
  // gPTPCmd.ptpMode = MOVJ_XYZ;
  gPTPCmd.ptpMode = MOVJ_XYZ;
  gPTPCmd.x = x;
  gPTPCmd.y = y;
  gPTPCmd.z = z;
  gPTPCmd.r = r;

  Serial.print("move to x:"); Serial.print(gPTPCmd.x); Serial.print(" y:"); Serial.print(gPTPCmd.y); Serial.print(" z:"); Serial.println(gPTPCmd.z);

  SetPTPCmd(&gPTPCmd, true, &gQueuedCmdIndex);
  ProtocolProcess();
  
  currentX = x;
  currentY = y;
  currentZ = z;
  currentR = r;
}

void movejoint(double joint1, double joint2, double joint3, double joint4)
{
  gPTPCmd.ptpMode = MOVJ_ANGLE;
  
  gPTPCmd.x = joint1;
  gPTPCmd.y = joint2;
  gPTPCmd.z = joint3;
  gPTPCmd.r = joint4;

  Serial.print("move to joint1:"); Serial.print(gPTPCmd.x); Serial.print(" joint2:"); Serial.print(gPTPCmd.y); Serial.print(" joint3:"); Serial.println(gPTPCmd.z);

  SetPTPCmd(&gPTPCmd, true, &gQueuedCmdIndex);
  ProtocolProcess();

  currentjoint1 = joint1;
  currentjoint2 = joint2;
  currentjoint3 = joint3;
  currentjoint4 = joint4;
  
}

// Function to retrieve and print the current pose
void printCurrentPose()
{
    if (bot.getPose()) {
      Serial.println("pose: ");
      Serial.print("x");Serial.println(bot.x);
      Serial.print("y");Serial.println(bot.y);
      Serial.print("z");Serial.println(bot.z);
      Serial.print("r");Serial.println(bot.r);
    }
}


void suck() {
    if (end == false) {
        s = !s;
        _set_end_effector_suction_cup(s);
        ProtocolProcess();
        delay(100);
    }
}

void sucks(bool enable) {
        _set_end_effector_suction_cup(enable);
        ProtocolProcess();
        // delay(100);
    
}

//ak
void button() {
  
  //spare 公仔
  // int buttonY = digitalRead(4);
  // int buttonG = digitalRead(50);
  // int buttonR = digitalRead(51);
  // int buttonB = digitalRead(10);
  // int buttonW = digitalRead(13);

  //骰仔 + 公仔
  int buttonY = digitalRead(4);
  int buttonG = digitalRead(42);
  int buttonR = digitalRead(51);
  int buttonB = digitalRead(13);
  int buttonW = digitalRead(50);

  if (buttonG == 0) {
    bot.getPose();
    printCurrentPose();
    // moveArm(bot.x,bot.y+25,bot.z,90);
    moveArm(bot.x,bot.y-30,bot.z,90);
    clear();
    Serial.println("Button G pressed");
    delay(1000); // Add delay to prevent rapid button presses
  }
  if (buttonY == 0) {
    bot.getPose();
    printCurrentPose();
    moveArm(bot.x,bot.y+25,bot.z,90);
    // moveArm(bot.x,bot.y-30,bot.z,90);
    clear();
    Serial.println("Button Y pressed");
    delay(1000); // Add delay to prevent rapid button presses
  }
  if (buttonR == 0) {
    bot.getPose();
    printCurrentPose();
    moveArm(bot.x+25,bot.y,bot.z,90);
    // moveArm(bot.x,bot.y-30,bot.z,90);
    clear();
    Serial.println("Button R pressed");
    delay(1000); // Add delay to prevent rapid button presses
  }
  if (buttonB == 0) {
    bot.getPose();
    printCurrentPose();
    moveArm(bot.x-20,bot.y,bot.z,90);
    // moveArm(bot.x,bot.y+25,bot.z,90);
    clear();
    Serial.println("Button B pressed");
    delay(1000); // Add delay to prevent rapid button presses
  }
  // if (buttonW == 1 && buttonG == 1 && buttonB == 1 && buttonY == 1 && buttonR == 1)
  //   sucks(true);
  
  if (buttonW == 0) {
    clear();
    bot.getPose();
    printCurrentPose();
    moveArm(bot.x,bot.y,-10,90); //box pp 
    // moveArm(bot.x,bot.y,-50,90); //stamps
    delay(1500); 
    suck();
    delay(300);
    moveArm(bot.x,bot.y,70,90);
    Serial.println("Button W pressed");
    delay(1000); // Add delay to prevent rapid button presses
  }
}

void loop(){
  button();
}