/*
  dobotMag.h - Library for controlling the Dobot Magician (https://www.dobot.cc/)
  Created by Matthew Li, 2020.1.28.
  Released into the public domain.
  Serial port is used to connect to the computer for debugging (serial monitor).
  Serial port 1 is used to connect to the Dobot.
*/
#ifndef dobotMag_h
#define dobotMag_h

#include "Arduino.h"

// JUMP mode, (x,y,z,r) is the target point in Cartesian coordinate system
#define MODE_PTP_JUMP_XYZ 0x00
// MOVJ mode, (x,y,z,r) is the target point in Cartesian coordinate system
#define MODE_PTP_MOVJ_XYZ 0x01
// MOVL mode, (x,y,z,r) is the target point in Cartesian coordinate system
#define MODE_PTP_MOVL_XYZ 0x02

// JUMP mode, (x,y,z,r) is the target point in Joint coordinate system
#define MODE_PTP_JUMP_ANGLE 0x03
// MOVJ mode, (x,y,z,r) is the target point in Joint coordinate system
#define MODE_PTP_MOVJ_ANGLE 0x04
// MOVL mode, (x,y,z,r) is the target point in Joint coordinate system
#define MODE_PTP_MOVL_ANGLE 0x05

// MOVJ mode, (x,y,z,r) is the angle increment in Joint coordinate system
#define MODE_PTP_MOVJ_INC 0x06
// MOVL mode, (x,y,z,r) is the Cartesian coordinate increment in Cartesian coordinate system
#define MODE_PTP_MOVL_INC 0x07
// MOVJ mode, (x,y,z,r) is the Cartesian coordinate increment in Cartesian coordinate system
// vibrate heavily
#define MODE_PTP_MOVJ_XYZ_INC 0x08
// JUMP mode, (x,y,z,r) is the Cartesian coordinate increment in Cartesian coordinate system
#define MODE_PTP_JUMP_MOVL_XYZ 0x09

class dobotMag
{
  public:
    dobotMag(bool debugMode);
    void setHome();
    void setQueuedCmdStartExec();
    void setQueuedCmdClear();
    void setPTPJointParams();
    void setPTPCoordinateParams();
    void setPTPCommonParams(float velocity, float acceleration);
    void setPTPJumpParams(float lift, float maxLift);
    void setHomeParams(float x, float y, float z, float r);
    bool getPose();
    void moveTo(float x, float y, float z, float r, byte mode, bool wait);
    float x, y, z, r, j1, j2, j3, j4;
    unsigned long currentIndex;
  private:
    void sendCommand(byte cmd[], int len);
    bool getResponse();
    bool getCurrentIndex();
};

#endif
