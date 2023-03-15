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
d.speed()

print('start')
movex = {
    '000000000': [0, 4, 2, 4, 6, 8], '100020000': [8], '001020000': [6],
    '000020100': [2], '000020001': [0],  '020010000': [0, 2],
    '000210000': [0, 6], '000012000': [2, 8], '000010020': [6, 8],
    '120010002': [3, 6], '021010200': [5, 8], '002210100': [7, 8],
    '100210002': [1, 2], '001012200': [1], '200012001': [7], '200010021': [5],
    '002010120': [3], '000020000': [0, 2, 6, 8], '200000000': [4],
    '002000000': [4], '000000200': [4], '000000002': [4],
    '002010200': [1, 3, 5, 7], '200010002': [1, 3, 5, 7], '000200100': [8],
    '000000021': [2], '001002000': [0], '120000000': [6], '000200121': [2],
    '001002021': [0], '121002000': [6], '120200100': [8], '000000120': [0],
    '000002001': [6], '021000000': [8], '100200000': [2], '100200120': [2],
    '000002121': [0], '021002001': [6], '121200000': [8]}


class Board:
  def __init__(self, test=0, r_v=1500, b_v=1500, first=1, x=265.3, y=45.5, z=-70, x_off=35.8, y_off=-39, upr=0.0, cx=50, cy=50, home=[140, 100,0]):
    self.test = test
    self.r_v = r_v
    self.b_v = b_v
    self.round = 0
    self.first = first
    self.blankcount = 0
    self.x, self.y, self.z = x, y, z
    self.upr = upr
    self.cx, self.cy = cx, cy
    self.x_off, self.y_off = x_off, y_off
    self.xupr, self.yupr = self.x_off/95, self.y_off/95
    self.cap = cv2.VideoCapture(0)
    self.home = home
    self.sit = 0
    self.pos = [(self.x, self.y+self.y_off * 3),
                (self.x+self.x_off, self.y+self.y_off * 3),
                (self.x+ 2 * x_off, self.y+self.y_off * 3),
                (self.x, self.y-self.y_off),
                (self.x+self.x_off, self.y-self.y_off),
                (self.x+ 2 * self.x_off, self.y-self.y_off)]
    self.checktemp = 0
    self.board = '0' * 9
    self.boardchecks = ['0' * 9] * 3
    self.grid = np.array([[0, 100, 200, 300], [0, 100, 200, 300]])



        
    
if __name__ == '__main__':
  print('end')
  d.close()


