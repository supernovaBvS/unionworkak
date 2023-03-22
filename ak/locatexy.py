import cv2
import numpy as np
import time
import pydobot
from serial.tools import list_ports

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[2].device

d = pydobot.Dobot(port)
d.suck(False)
d.speed(90,90)

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



class CheckersGame:
    def __init__(
        #self, test=0, z=-70, x=265.3 , y=45.5, x_offset=-35.8, y_offset=-39
        self, test=0, z=-50, x=300 , y=45, x_offset=-45, y_offset=-45,
        home=[200, -140, 0], first=1, r_value=1500, b_value=1500, upr=0.0,
            cx=150, cy=150,SITUATION_LOSE = 7, SITUATION_WIN = 8, SITUATION_DRAW = 6):
        self.test = test
        self.r_value = r_value  # color area threshold
        self.b_value = b_value  # ''

        self.round = 0  # moved count
        self.first = first  # is bot first
        self.blankcount = 0
        self.x, self.y, self.z = x, y, z  # grid #1 coordinates (top left of Dobot #1)

        # ** x, y, x_offset, y_offset must be as precise as possible for Dobot #1.

        self.upr = upr  # unit pixel ratio
        self.cx, self.cy = cx, cy  # grid #1 center image coordinates (normally (55, 55))
        self.x_offset, self.y_offset = x_offset, y_offset
        self.xupr, self.yupr = self.x_offset , self.y_offset   # unit pixel ratio
        self.cap = cv2.VideoCapture(0)

        self.home = home  # home position
        self.sit = 0  # situation id
        self.pos = [(self.x, self.y+self.y_offset*2-35),
                    (self.x+self.x_offset, self.y+self.y_offset*2-35),
                    (self.x+2*x_offset, self.y+self.y_offset*2-35),
                    (self.x, self.y+35),
                    (self.x+self.x_offset, self.y+35),
                    (self.x+2*self.x_offset, self.y+35)]  # default chess coordinates
        print (self.pos)
        self.checkattemp = 0  # saving checks
        self.checkerboard = '0' * 9  # checkerboard with color id
        self.checkerboardchecks = ['0' * 9] * 3  # list of self.checkattemp
        self.grid = np.array([[0, 100, 200, 300], [0, 100, 200, 300]])  # cropping


    def find_red_centers(img):
        # Convert image to HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Threshold for red color in HSV space
        lower_red = np.array([0, 70, 50])
        upper_red = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        
        lower_red = np.array([170, 70, 50])
        upper_red = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red, upper_red)
        
        mask = cv2.bitwise_or(mask1, mask2)
        
        # Find contours and filter for large enough area
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        centers = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1000:
                M = cv2.moments(cnt)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                centers.append((cy, cx))
        return centers

    def m(self):  # move
        # get
        d.suck(False)
        d.jump(self.pos[self.round][0], self.pos[self.round][1],self.z, 0)
        d.suck(True)
        d.movej(self.pos[self.round][0], self.pos[self.round][1],self.z+40, 0)
        time.sleep(2)

        # place
        d.jump(self.coor[0], self.coor[1]+5, self.z, 0)
        d.suck(False)

        # Find red checker coordinates and pick up
        img = d.getImage()
        red_centers = find_red_centers(img)
        if len(red_centers) == 0:
            print("No red checkers detected!")
            return
        x, y = self.x + (red_centers[0][1] - self.cx), self.y + (red_centers[0][0] - self.cy)
        d.jump(x, y, self.z, 0)
        d.suck(True)

        # Place checker in corresponding position
        if self.first:
            color = 1
            j = self.checkerboard.index('0')
        else:
            color = 2
            j = self.checkerboard.index('0', 5)
        pos_x, pos_y = self.pos[j][0], self.pos[j][1]
        d.jump(pos_x, pos_y, self.z, 0)
        d.suck(False)

        # Update game state
        self.checkerboard = self.checkerboard[:j] + str(color) + self.checkerboard[j+1:]
        self.checkerboardv[j // 3, j % 3] = color
        self.sit += 1
        self.first = not self.first
        self.checkerboardchecks.pop(0)
        self.checkerboardchecks.append(self.checkerboard)
        self.checkattemp += 1
        self.blankcount = 0

        # Clear checkerboard if game is over
        if self.check(getCenter=False) != 0:
            self.checkerboardv, self.checkerboard = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]), '0' * 9
            self.checkerboardchecks = ['0' * 9] * 3
            self.checkattemp = 0
            self.round = 0
            self.blankcount = 0
            self.end()
        else:
            self.round += 1

