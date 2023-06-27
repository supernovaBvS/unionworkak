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
# d.grip(False)
d.speed()

print('start')
# z= -70
# x= 270
# y= 41
# x_offset= -35
# y_offset= -45
# pos = [(x+2, y+y_offset*2-35),
#         (x+x_offset, y+y_offset*2-35),
#         (x+2*x_offset, y+y_offset*2-35),
#         (x, y+43),
#         (x+x_offset, y+43),
#         (x+2*x_offset, y+43)]

# x, y, z, r = (252.32359313964844, -0.5828672051429749, -28.928955078125, -0.13235294818878174)
#     hx, hy = pos[i]
#     d.jump(hx, hy, z,0)
#     d.grip(True)
# #     d.suck(True)
#     time.sleep(2)
#     d.jump(250, 0, z+25,0)
#     d.grip(False)
# #     d.suck(False)
#     time.sleep(2)
# d.grip(False)


# d.jump(x,y+20,z,r)
# d.grip(True)
# d.jump(x,y-20,z,r)

d.jump(250, 0, 50,0)
d.suck(False)
d.close()
print('end')