import time
import pydobot
from serial.tools import list_ports

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[2].device

d = pydobot.Dobot(port)
d.suck(False)
d.speed()

print('start')

def setuppp():
  Px, Py, Pz, px, py, pz = (203, -65, -50, 203, 100, -45)
  Bx, By, Bz, bx, by, bz = (216, 75, -45, 216, -110, -50)
  return Px, Py, Pz, px, py, pz, Bx, By, Bz, bx, by, bz


def main():
  for k in range(1):
    for j in range(2):
      for i in range(2):
        d.suck(False)
        d.jump(Px+(j*30), Py-(i*30), Pz, 90)
        d.suck(True)
        d.jump(Px+(j*30), Py-(i*30), Pz+50, 90)
        d.jump(px+(j*30), py-(i*30), pz, 90)
        d.suck(False)

        
def back():
  for k in range(1):
    for j in range(2):
      for i in range(2):
        d.suck(False)
        d.jump(Bx+(j*30), By+(i*30), Bz, 90)
        d.suck(True)
        d.jump(Bx+(j*30), By+(i*30), Bz+50, 90)
        d.jump(bx+(j*30), by+(i*30), bz, 90)
        d.suck(False)

        
    
if __name__ == '__main__':
  # while True:
    # print(d.get_pose().position[0:4])
  Px, Py, Pz, px, py, pz, Bx, By, Bz, bx, by, bz = setuppp()
  main()
  # back()
  d.jump(250,0,70)
  d.close()


