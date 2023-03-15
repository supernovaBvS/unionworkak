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




if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    hx, hy, hz = [140, 100, 0]
    d.movej(hx, hy, hz)
    while True:
        # Grab the webcameras image.
        frame = cap.read()[1]
        # Resize the raw image into (224-height,224-width) pixels.
        # Show the image in a window
        # cv2.imshow('Image', frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    d.movej(250,0,70)
    print('end')
    d.close()