# version: Python3
from DobotEDU import *

class Gripper:
    def __init__(self):
        self.op_command = m_lite.set_endeffector_gripper(enable=True, on=False)
        self.close_command = m_lite.set_endeffector_gripper(enable=True, on=True)
    
    def on(self):
        op = m_lite.set_endeffector_gripper(enable=True, on=False)
    
    def off(self):
        close = m_lite.set_endeffector_gripper(enable=True, on=True)
        
        
class Suction:
    def __init__(self):
        self.op_command = m_lite.set_endeffector_suctioncup(enable=True, on=False)
        self.close_command = m_lite.set_endeffector_suctioncup(enable=True, on=True)
    
    def off(self):
        op = m_lite.set_endeffector_suctioncup(enable=True, on=False)
    
    def on(self):
        close = m_lite.set_endeffector_suctioncup(enable=True, on=True)
        
def home():
  return m_lite.set_homecmd()


def getpose():
  gp = m_lite.get_pose()
  x, y, z = gp['x'], gp['y'], gp['z']
  return x, y, z


def jump(x, y, z):
  return m_lite.set_ptpcmd(ptp_mode=0, x=x, y=y, z=z, r=90)


def pick():
  return getpose()
  
  
def place():
  return getpose()
  
  
def setuppp():
  px, py, pz = pick()
  time.sleep(7)
  bx, by, bz = place()
  return px, py, pz, bx, by, bz


def pickandplace():
  i = j = 0
  for k in range(5):
    jump(px, py, pz-i*25)
    time.sleep(1)
    gripper.off()
    jump(bx, by, bz+j*25)
    gripper.on()
    time.sleep(2)
    j+=1
    i+=1
    
    
if __name__ == '__main__':
  gripper = Gripper()
  px, py, pz, bx, by, bz = setuppp()
  pickandplace()
  home()



































