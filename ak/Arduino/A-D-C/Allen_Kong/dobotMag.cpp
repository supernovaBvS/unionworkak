/*
  dobotMag.cpp - Library for controlling the Dobot Magician (https://www.dobot.cc/)
  Created by Matthew Li, 2020.1.28.
  Released into the public domain.
  Serial port is used to connect to the computer for debugging (serial monitor).
  Serial port 1 is used to connect to the Dobot.
*/

#include "Arduino.h"
#include "dobotMag.h"

// maximum waiting time for waiting response after sending command
#define MAXWAITINGTIME 1000

bool _debugMode;

// 0xAA 0xAA len ID CTRL params payload_checksum
// len = length of ID, CTRL and params only.  Total number of bytes = len+4
// the bit 0 of Ctrl is rw (0=read,1=write), the bit 1 of Ctrl is isQueue (0=immediate, 1=queued)
// When isQueue = 1,that indicats the instruction is a queue command,which returns a 64-bit index. So the length is 2+8.
// When isQueue = 0, the instruction is an immediate command, which has no return. So the length is 2+0.
// payload_checksum = 256-sum of (ID, CTRL, params)
byte setHomeCmd[]={0xAA,0xAA,0x06,0x1F,0x03,0x00,0x00,0x00,0x00,0xDE}; // ID 31
byte getPoseCmd[]={0xAA,0xAA,0x02,0x0A,0x00,0xF6}; // ID 10
byte setQueuedCmdStartExecCmd[]={0xAA,0xAA,0x02,0xF0,0x01,0x0F}; // ID 240
byte setQueuedCmdClearCmd[]={0xAA,0xAA,0x02,0xF5,0x01,0x0A}; // ID 245
byte setPTPCmd[]={0xAA,0xAA,0x13,0x54,0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF}; // ID 84
byte setPTPJointParamsCmd[]={0xAA,0xAA,0x22,0x50,0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF}; // ID 80
byte setPTPCoordinateParamsCmd[]={0xAA,0xAA,0x12,0x51,0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF}; // ID 81
byte setPTPCommonParamsCmd[]={0xAA,0xAA,0x0A,0x53,0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF}; // ID 83
byte setPTPJumpParamsCmd[]={0xAA,0xAA,0x0A,0x52,0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF}; // ID 82
byte setHomeParamsCmd[]={0xAA,0xAA,0x12,0x1E,0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF}; // ID 30
byte getCurrentIndexCmd[]={0xAA,0xAA,0x02,0xF6,0x00,0x0A}; // ID 246

#define MAXRETURNEDDATALEN 64
byte returnedData[MAXRETURNEDDATALEN];
int returnedDataLen;

// The current queue index is 64 bit unsigned long long.  The index is reset to zero when the Dobot is powered up.
// uint64_t currentIndex = 0x0123456789abcdefULL;
// Due to the limitation of Arduino, unsigned long is used to store the currentIndex

// debugMode=true, debug messages are printed at the Serial port
dobotMag::dobotMag(bool debugMode)
{
    _debugMode=debugMode;
    x=y=z=r=0;
    j1=j2=j3=j4=0;
    currentIndex=0;
}

void dobotMag::setQueuedCmdStartExec() {
  sendCommand(setQueuedCmdStartExecCmd,sizeof(setQueuedCmdStartExecCmd));
  getResponse();
}

void dobotMag::setQueuedCmdClear() {
  sendCommand(setQueuedCmdClearCmd,sizeof(setQueuedCmdClearCmd));
  getResponse();
}

// Set the playback speed parameters, including the velocity and acceleration of joint coordinate axes.
// The speed set by this command is only applied to playback motion and does not work for the jogging movement.
// joint velocity of 4 axis, joint acceleration of 4 axis are all set to 200
void dobotMag::setPTPJointParams() {
  float f=200.0;
  unsigned int checksum=0;
  setPTPJointParamsCmd[5]=setPTPJointParamsCmd[9]=setPTPJointParamsCmd[13]=setPTPJointParamsCmd[17]=setPTPJointParamsCmd[21]=setPTPJointParamsCmd[25]=setPTPJointParamsCmd[29]=setPTPJointParamsCmd[33]=*(byte *)&f;
  setPTPJointParamsCmd[6]=setPTPJointParamsCmd[10]=setPTPJointParamsCmd[14]=setPTPJointParamsCmd[18]=setPTPJointParamsCmd[22]=setPTPJointParamsCmd[26]=setPTPJointParamsCmd[30]=setPTPJointParamsCmd[34]=*(((byte *)&f)+1);
  setPTPJointParamsCmd[7]=setPTPJointParamsCmd[11]=setPTPJointParamsCmd[15]=setPTPJointParamsCmd[19]=setPTPJointParamsCmd[23]=setPTPJointParamsCmd[27]=setPTPJointParamsCmd[31]=setPTPJointParamsCmd[35]=*(((byte *)&f)+2);
  setPTPJointParamsCmd[8]=setPTPJointParamsCmd[12]=setPTPJointParamsCmd[16]=setPTPJointParamsCmd[20]=setPTPJointParamsCmd[24]=setPTPJointParamsCmd[28]=setPTPJointParamsCmd[32]=setPTPJointParamsCmd[36]=*(((byte *)&f)+3);
  checksum=0;
  for (int i=3;i<37;i++) {
    checksum+=setPTPJointParamsCmd[i];
  }
  checksum = 256 - (checksum % 256);
  setPTPJointParamsCmd[37]=checksum;
  sendCommand(setPTPJointParamsCmd,sizeof(setPTPJointParamsCmd));
  getResponse();
}

// This command is to set the velocity and acceleration of the Cartesian coordinate axes in PTP mode
//In PTP mode, coordinate velocity of xyz 3 axis, end-effector velocity, coordinate acceleration of xyz 3 axis, end-effector acceleration
// are all set to 200
void dobotMag::setPTPCoordinateParams() {
  float f=200.0;
  unsigned int checksum=0;
  setPTPCoordinateParamsCmd[5]=setPTPCoordinateParamsCmd[9]=setPTPCoordinateParamsCmd[13]=setPTPCoordinateParamsCmd[17]=*(byte *)&f;
  setPTPCoordinateParamsCmd[6]=setPTPCoordinateParamsCmd[10]=setPTPCoordinateParamsCmd[14]=setPTPCoordinateParamsCmd[18]=*(((byte *)&f)+1);
  setPTPCoordinateParamsCmd[7]=setPTPCoordinateParamsCmd[11]=setPTPCoordinateParamsCmd[15]=setPTPCoordinateParamsCmd[19]=*(((byte *)&f)+2);
  setPTPCoordinateParamsCmd[8]=setPTPCoordinateParamsCmd[12]=setPTPCoordinateParamsCmd[16]=setPTPCoordinateParamsCmd[20]=*(((byte *)&f)+3);
  checksum=0;
  for (int i=3;i<21;i++) {
    checksum+=setPTPCoordinateParamsCmd[i];
  }
  checksum = 256 - (checksum % 256);
  setPTPCoordinateParamsCmd[21]=checksum;
  sendCommand(setPTPCoordinateParamsCmd,sizeof(setPTPCoordinateParamsCmd));
  getResponse();
}        

// This command is to set the velocity ratio and the acceleration ratio in PTP mode
// This command can be used to alter the velocity and the acceleration of the Dobot after initialization
void dobotMag::setPTPCommonParams(float velocity, float acceleration) {
  unsigned int checksum=0;
  setPTPCommonParamsCmd[5]=*(byte *)&velocity;
  setPTPCommonParamsCmd[6]=*(((byte *)&velocity)+1);
  setPTPCommonParamsCmd[7]=*(((byte *)&velocity)+2);
  setPTPCommonParamsCmd[8]=*(((byte *)&velocity)+3);
  setPTPCommonParamsCmd[9]=*(byte *)&acceleration;
  setPTPCommonParamsCmd[10]=*(((byte *)&acceleration)+1);
  setPTPCommonParamsCmd[11]=*(((byte *)&acceleration)+2);
  setPTPCommonParamsCmd[12]=*(((byte *)&acceleration)+3);
  checksum=0;
  for (int i=3;i<13;i++) {
    checksum+=setPTPCommonParamsCmd[i];
  }
  checksum = 256 - (checksum % 256);
  setPTPCommonParamsCmd[13]=checksum;
  sendCommand(setPTPCommonParamsCmd,sizeof(setPTPCommonParamsCmd));
  getResponse();
}

// This command is to set the lifting height and maximum lifting height in JUMP mode
void dobotMag::setPTPJumpParams(float lift, float maxLift) {
  unsigned int checksum=0;
  setPTPJumpParamsCmd[5]=*(byte *)&lift;
  setPTPJumpParamsCmd[6]=*(((byte *)&lift)+1);
  setPTPJumpParamsCmd[7]=*(((byte *)&lift)+2);
  setPTPJumpParamsCmd[8]=*(((byte *)&lift)+3);
  setPTPJumpParamsCmd[9]=*(byte *)&maxLift;
  setPTPJumpParamsCmd[10]=*(((byte *)&maxLift)+1);
  setPTPJumpParamsCmd[11]=*(((byte *)&maxLift)+2);
  setPTPJumpParamsCmd[12]=*(((byte *)&maxLift)+3);
  checksum=0;
  for (int i=3;i<13;i++) {
    checksum+=setPTPJumpParamsCmd[i];
  }
  checksum = 256 - (checksum % 256);
  setPTPJumpParamsCmd[13]=checksum;
  sendCommand(setPTPJumpParamsCmd,sizeof(setPTPJumpParamsCmd));
  getResponse();
}

// This command is to set homing position.
void dobotMag::setHomeParams(float x, float y, float z, float r) {
  unsigned int checksum=0;
  setHomeParamsCmd[5]=*(byte *)&x;
  setHomeParamsCmd[6]=*(((byte *)&x)+1);
  setHomeParamsCmd[7]=*(((byte *)&x)+2);
  setHomeParamsCmd[8]=*(((byte *)&x)+3);
  setHomeParamsCmd[9]=*(byte *)&y;
  setHomeParamsCmd[10]=*(((byte *)&y)+1);
  setHomeParamsCmd[11]=*(((byte *)&y)+2);
  setHomeParamsCmd[12]=*(((byte *)&y)+3);
  setHomeParamsCmd[13]=*(byte *)&z;
  setHomeParamsCmd[14]=*(((byte *)&z)+1);
  setHomeParamsCmd[15]=*(((byte *)&z)+2);
  setHomeParamsCmd[16]=*(((byte *)&z)+3);
  setHomeParamsCmd[17]=*(byte *)&r;
  setHomeParamsCmd[18]=*(((byte *)&r)+1);
  setHomeParamsCmd[19]=*(((byte *)&r)+2);
  setHomeParamsCmd[20]=*(((byte *)&r)+3);
  checksum=0;
  for (int i=3;i<21;i++) {
    checksum+=setHomeParamsCmd[i];
  }
  checksum = 256 - (checksum % 256);
  setHomeParamsCmd[21]=checksum;
  sendCommand(setHomeParamsCmd,sizeof(setHomeParamsCmd));
  getResponse();
}

void dobotMag::setHome() {
  bool status;
  unsigned long queueIndex;
	sendCommand(setHomeCmd,sizeof(setHomeCmd));
  status=getResponse();
  if (status) {
    queueIndex=*(unsigned long *)&returnedData[5];
    do {
      delay(1000);
      while (!getCurrentIndex())
        delay(100);
      if (_debugMode) {
        Serial.print("waiting ");
        Serial.print(currentIndex);
        Serial.print(':');
        Serial.println(queueIndex);
      }
    } while (currentIndex<queueIndex);
  } else {
    delay(15000); // abnormal case, no response and current index is not returned
  }
}


void dobotMag::moveTo(float x, float y, float z, float r, byte mode, bool wait) {
  bool status;
  unsigned long queueIndex;
  float f;
  unsigned int checksum=0;
  setPTPCmd[5]=mode;
  f=x;
  setPTPCmd[6]=*(byte *)&f;
  setPTPCmd[7]=*(((byte *)&f)+1);
  setPTPCmd[8]=*(((byte *)&f)+2);
  setPTPCmd[9]=*(((byte *)&f)+3);
  f=y;
  setPTPCmd[10]=*(byte *)&f;
  setPTPCmd[11]=*(((byte *)&f)+1);
  setPTPCmd[12]=*(((byte *)&f)+2);
  setPTPCmd[13]=*(((byte *)&f)+3);
  f=z;
  setPTPCmd[14]=*(byte *)&f;
  setPTPCmd[15]=*(((byte *)&f)+1);
  setPTPCmd[16]=*(((byte *)&f)+2);
  setPTPCmd[17]=*(((byte *)&f)+3);
  f=r;
  setPTPCmd[18]=*(byte *)&f;
  setPTPCmd[19]=*(((byte *)&f)+1);
  setPTPCmd[20]=*(((byte *)&f)+2);
  setPTPCmd[21]=*(((byte *)&f)+3);
  checksum=0;
  for (int i=3;i<22;i++) {
    checksum+=setPTPCmd[i];
  }
  checksum = 256 - (checksum % 256);
  setPTPCmd[22]=checksum;

  sendCommand(setPTPCmd,sizeof(setPTPCmd));

  status=getResponse();
  if (wait) {
    if (status) {
      queueIndex=*(unsigned long *)&returnedData[5];
      do {
        delay(200);
        while (!getCurrentIndex())
          delay(100);
        if (_debugMode) {
          Serial.print("waiting ");
          Serial.print(currentIndex);
          Serial.print(':');
          Serial.println(queueIndex);
        }
      } while (currentIndex<queueIndex);
    } else {
      delay(3000); // abnormal case, no response and current index is not returned
    }
  }
}

bool dobotMag::getPose() {
  bool status;
  sendCommand(getPoseCmd,sizeof(getPoseCmd));
  status=getResponse();
  if (_debugMode) {
    Serial.print("Get pose status: ");
    Serial.println(status);
    for (int i=0;i<returnedDataLen;i++) {
      Serial.print(returnedData[i],HEX);
      Serial.print(" ");
    }
    Serial.println();
  }
  if (status) {
    // value of the float pointer of address returnedData[5]
    x=*(float *)&returnedData[5];
    y=*(float *)&returnedData[9];
    z=*(float *)&returnedData[13];
    r=*(float *)&returnedData[17];
    j1=*(float *)&returnedData[21];
    j2=*(float *)&returnedData[25];
    j3=*(float *)&returnedData[29];
    j4=*(float *)&returnedData[33];
  }
  else {
    x=y=z=r=j1=j2=j3=j4=0;
  }
  return status;
}

//-------------------- private ----------------------

// send command to Dobot, parameter: command, sizeof(command)
void dobotMag::sendCommand(byte cmd[], int len) {
  if (_debugMode) Serial.print("Send to Dobot: ");
  for(int i = 0; i < len; i++) {
    Serial1.print(char(cmd[i])); // the byte must be converted to char type, else numeric value (digits) are sent
    if (_debugMode) {
      Serial.print(cmd[i],HEX);
      Serial.print(' ');    
    }
  }
  if (_debugMode) Serial.println();
}

// get response from Dobot
// returned data stored at returnedData[]
// lenght check and checksum are validated
// success: return true, fail: return false
bool dobotMag::getResponse() {
  unsigned long readDataTimer;
  byte data;
  unsigned int MAXWAITABYTE=50;
  unsigned int checksum=0;
  returnedDataLen=0;

  // check if any data returned within limited time
  readDataTimer=millis();
  while (!Serial1.available()) {
      if (millis()>MAXWAITINGTIME+readDataTimer || millis()<readDataTimer) {
          if (_debugMode) Serial.println("Dobot error: no data returned.");
          return false;
      }
  }

  if (_debugMode) Serial.print("Get from Dobot: ");

  while (Serial1.available()) {
    data=Serial1.read();
    returnedData[returnedDataLen++]=data;
    if (returnedDataLen==MAXRETURNEDDATALEN)
        break;
    if (_debugMode) Serial.print(data,HEX);
    if (_debugMode) Serial.print(" "); 
    // wait for more data
    readDataTimer=millis();   
    while (!Serial1.available()) {
      if (millis()>MAXWAITABYTE+readDataTimer || millis()<readDataTimer) {
          break;
      }
    }
  }
  if (_debugMode) Serial.println();

  if (returnedData[0]!=0xAA || returnedData[1]!=0xAA || returnedData[2]+4!=returnedDataLen)
    return false;
  checksum=0;
  for (int i=3;i<returnedDataLen-1;i++) {
    checksum+=returnedData[i];
  }
  checksum = 256 - (checksum % 256);
  if (returnedData[returnedDataLen-1]!=checksum)
    return false;
  return true;
}

// if failed to get response, false is returned.  This happens sometimes.
// There is a 64-bit internal count index in Dobot controller command queue mechanism.
// The counter is automatically incremented after the controller executes a command.
bool dobotMag::getCurrentIndex() {
  bool status;
  // This command uses immediate mode.
  sendCommand(getCurrentIndexCmd,sizeof(getCurrentIndexCmd));
  status=getResponse();
  if (status) {
    currentIndex=*(unsigned long *)&returnedData[5];
    return true;
  } else
    return false;
}
