import cv2
import random
import time
import numpy as np
import pydobot
from serial.tools import list_ports

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[2].device

d = pydobot.Dobot(port)
d.suck(False)
d.grip(False)
d.speed()

print('start')
z= -50
x= 300
y= 41
x_offset= -45
y_offset= -45
pos = [(x+2, y+y_offset*2-35),
        (x+x_offset, y+y_offset*2-35),
        (x+2*x_offset, y+y_offset*2-35),
        (x, y+43),
        (x+x_offset, y+43),
        (x+2*x_offset, y+43)]
for i in range(len(pos)):
    hx, hy = pos[i]
    d.jump(hx, hy, z+10,0)
    d.grip(True)
    time.sleep(2)
    d.jump(250, 0, 70,0)
    d.grip(False)
    time.sleep(2)

d.close()
print('end')