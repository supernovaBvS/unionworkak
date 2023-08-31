# version: Python3
from DobotEDU import *

class Gripper:
    def __init__(self):
        self.op_command = magician.set_endeffector_gripper(enable=True, on=False)
        self.close_command = magician.set_endeffector_gripper(enable=True, on=True)
    
    def on(self):
        op = magician.set_endeffector_gripper(enable=True, on=False)
    
    def off(self):
        close = magician.set_endeffector_gripper(enable=True, on=True)
        
        
class Suction:
    def __init__(self):
        self.op_command = magician.set_endeffector_suctioncup(enable=True, on=False)
        self.close_command = magician.set_endeffector_suctioncup(enable=True, on=True)
    
    def off(self):
        op = magician.set_endeffector_suctioncup(enable=True, on=False)
    
    def on(self):
        close = magician.set_endeffector_suctioncup(enable=True, on=True)
        
        
def home():
  jump(250,0,0,90)
  magician.clear_alarm()


def getpose():
  gp = magician.get_pose()
  x, y, z = gp['x'], gp['y'], gp['z']
  return x, y, z


def jump(x, y, z, r):
  return magician.ptp(mode=0, x=x, y=y, z=z, r=r)


def pick():
  return getpose()
  
  
def place():
  return getpose()
  
  
def setuppp():
  Px, Py, Pz, px, py, pz = (216, -75, -50, 216, 100, -45)
  Bx, By, Bz, bx, by, bz = (216, 65, -45, 216, -110, -50)
  return Px, Py, Pz, px, py, pz, Bx, By, Bz, bx, by, bz


def main1():
  i = j = 0
  for k in range(1):
    # jump(px, py, pz-i*25, 90)
    jump(Px, Py, Pz, 90)
    time.sleep(1)
    suction.off()
    jump(px, py, pz+j*25, 90)
    gripper.on()
    time.sleep(2)
    j+=1
    i+=1
    
    
def main():
  for k in range(1):
    for j in range(2):
      for i in range(2):
        suction.off()
        jump(Px+(j*30), Py-(i*30), Pz, 90)
        suction.on()
        jump(px+(j*30), py-(i*30), pz, 90)
        suction.off() 

        
def back():
  for k in range(1):
    for j in range(2):
      for i in range(2):
        suction.off()
        jump(Bx+(j*30), By+(i*30), Bz, 90)
        suction.on()
        jump(bx+(j*30), by+(i*30), bz, 90)
        suction.off()        
        
    
if __name__ == '__main__':
  suction = Suction()
  Px, Py, Pz, px, py, pz, Bx, By, Bz, bx, by, bz = setuppp()
  main()
  back()
  home()