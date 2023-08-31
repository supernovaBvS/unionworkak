import time
import pydobot
from serial.tools import list_ports

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[-1].device

d = pydobot.Dobot(port)
d.suck(False)
d.speed()

print('start')

d._set_end_effector_gripper(True)