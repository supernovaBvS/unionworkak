
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

//#define JOG_STICK
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


//////// Prie kokiu pirminiu kordinaciu suprogramuota sistema  ////////////////////////////
double dx_home = 212.2 ;     
double dy_home = 0;   
double dz_home = 199.8;   
double dr_home = 0;

double djoint1_home = 0.0;     
double djoint2_home = 0;   
double djoint3_home = 0;   
double djoint4_home = 0;
////////////////////////////////////////////////////////////////////////

double joint1_ofset = 0;

const byte kCmdSetHOMEParams = 13;
const byte kCmdHOMECmd = 15;
const int kDataLength = 21;

int xhome_mygtuko_pin = 22;
int yhome_mygtuko_pin = 24;

int xhome_mygtukas;
int yhome_mygtukas;
int led = 13;
int rusiavimo_optikos_pin = 2;
int rusiavimo_optika = 0;

double darbinis_point[4] = {-1.8697, 15.4835 , 0.4057, 0};  // JOINT 
double paeimimo_point[4] = {42.2502, 15.4835 , 0.4057 ,0};  // JOINT

double spalvos_check_point[4] = {275.4106, -85.6843, 16.00, 0};       //kordinates
double belt_point[4] = {198.0025, -85.9966, 20.2917, 0};                //kordinates

double rusiavimo_point[4] = {96.8348, 17.2430, -15.0020, 0};   //Joint
double rusiavimo_darbinis[4] = {119.5397, 9.1100, 1.5026, 0};   //Joint

double rusiavimo_paemimas[4] = {-104.2169, 173.8897, 5.6488, 0};   //kordinates

double kubelio_skirtumas = 24.5; 

int rusiavimo_tvarka[4] = {3,1,2,4};
int kubeliu_skaicius_rusiavime[4] = {0,0,0,0};    
// Spalvu kodai
// 1 - raudona
// 2 - geltona
// 3 - zalia
// 4 - melyna

double rusiavimo_point1[4] = {26.4671, 236.8331  , -43.00   , 0};
double rusiavimo_point2[4] = {-11.0449, 238.8970 , -41.00   , 0};
double rusiavimo_point3[4] = {-48.3414, 240.8172 , -42.00   , 0};
double rusiavimo_point4[4] = {-84.0542, 243.0042 , -42.00   , 0};

double rusiavimo_kordinates[4][4] {        //cartesian cordinate
  {rusiavimo_point1[0], rusiavimo_point1[1], rusiavimo_point1[2], rusiavimo_point1[3]},
  {rusiavimo_point2[0], rusiavimo_point2[1], rusiavimo_point2[2], rusiavimo_point2[3]},
  {rusiavimo_point3[0], rusiavimo_point3[1], rusiavimo_point3[2], rusiavimo_point3[3]},
  {rusiavimo_point4[0], rusiavimo_point4[1], rusiavimo_point4[2], rusiavimo_point4[3]},
 };

int Detuve[] = {0, 0, 0, 0, 0, 0, 0, 0, 0};

int pirma_eile = 123;
int antra_eile = 0;
int trecia_eile = 0;

bool start_komanda = true;

// kordinates

double point1[4] = {215.1404, 124.0499 , -45.00   , 0};
double point2[4] = {175.6577, 125.5617 , -45.00   , 0};
double point3[4] = {137.4507, 128.8269 , -45.00   , 0};
double point4[4] = {216.8926, 164.9008 , -45.00   , 0};
double point5[4] = {177.3893, 168.3094 , -45.00   , 0};
double point6[4] = {137.2848, 169.9191 , -45.00   , 0};
double point7[4] = {216.3909, 204.7939 , -46.00   , 0};
double point8[4] = {179.3857, 207.6078 , -46.00   , 0};
double point9[4] = {138.1540, 209.4336 , -49.00   , 0};

double Detuves_kordinates[9][4] = {        //cartesian cordinate
  {point1[0], point1[1], point1[2], point1[3]},
  {point2[0], point2[1], point2[2], point2[3]},
  {point3[0], point3[1], point3[2], point3[3]},
  {point4[0], point4[1], point4[2], point4[3]},
  {point5[0], point5[1], point5[2], point5[3]},
  {point6[0], point6[1], point6[2], point6[3]},
  {point7[0], point7[1], point7[2], point7[3]},
  {point8[0], point8[1], point8[2], point8[3]},
  {point9[0], point9[1], point9[2], point9[3]},
 };

/*********************************************************************************************************
** Function name:       setup
** Descriptions:        Initializes Serial
** Input parameters:    none
** Output parameters:   none
** Returned value:      none
*********************************************************************************************************/
// TCS230 or TCS3200 pins wiring to Arduino
#define S0 4
#define S1 5
#define S2 6
#define S3 7

// // Stores frequency read by the photodiodes
// int redFrequency = 0;
// int greenFrequency = 0;
// int blueFrequency = 0;

// int raudona[6]={15,40,45,110,38,80};

// int geltona[6]={15,30,20,35,28,50};

// int zalia[6]={40,70,30,55,48,85};

// int melyna[6]={35,80,40,68,15,38};

// int aptikta_spalva = 0;
// bool buvo_aptikta = false;
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
  Serial2.begin(115200);

  // delay(1000);
  // Serial2.println("M310 1");
  // delay(4000);
  // Serial2.println("M313 80");
  
  printf_begin();
  //Set Timer Interrupt
  FlexiTimer2::set(100, Serialread);
  FlexiTimer2::start();
  Serial.println("Atnaujinta 2023-03-28 14:21");

  // pinMode(xhome_mygtuko_pin, INPUT_PULLUP);
  // pinMode(yhome_mygtuko_pin, INPUT_PULLUP);
  // pinMode(rusiavimo_optikos_pin, INPUT_PULLUP);
  //ak
  // Keyboard.begin();
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
   // Setting the outputs
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
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