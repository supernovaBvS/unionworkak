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
cap = cv2.VideoCapture(0)
hx, hy, hz = [140, 100,0]
d.movej(hx, hy, hz)

src = cv2.imread('/Users/dev/Desktop/union_work/git/unionworkak/tttoe.png')

def contour(self, src, lmask, umask, lmask1=0, umask1=0, getCentre=False):
    blurred = cv2.GaussianBlur(src, (5,5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lmask, umask)
    if lmask1 + umask1 != 0:
        mask1 = cv2.inRange(hsv, lmask1, umask1)
        mask = mask + mask1
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]

    if len(contours) > 0:
        contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(contour)
        if getCentre:
            Moments = cv2.moments(contour)
            if Moments['m00'] != 0:
                cX = int(Moments['m10'] / Moments['m00'])
                cY = int(Moments['m01'] / Moments['m00'])
            else:
                cX, cY = (self.cx, self.cy)
                return contour, area, (cX, cY)
        else:
            return contour, area
    else:
        if getCentre:
            return 0, 0, (False, False)
        else:
            return 0, 0

contour(src)
cv2.waitKey(0)
cap.release()