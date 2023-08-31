import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time
import tensorflow
from cvzone.ClassificationModule import Classifier
import time
import pydobot
from serial.tools import list_ports

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[-1].device

d = pydobot.Dobot(port)
d.speed()
end = 0
s = False
x, y, z, r = d.get_pose().position[0:4]
print(x, y, z, r)

print('start')



cap = cv2.VideoCapture(1)
detector = HandDetector(maxHands=1)
classifier = Classifier("/Users/dev/Desktop/union_work/git/unionworkak/ak/opencv/hand_sign/Model/keras_model.h5", "/Users/dev/Desktop/union_work/git/unionworkak/ak/opencv/hand_sign/Model/labels.txt")
offset = 20
imgSize = 300

folder = "/Users/dev/Desktop/union_work/git/unionworkak/ak/opencv/hand_sign/Data/C"
counter = 0

# labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
#           "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

labels = ["A", "B", "C", "I", "L", "U"]

def control_dobot():

    def left():
        x, y, z, r = d.get_pose().position[0:4]
        d.movej(x,y+10,z,r)
        d.clear_alarms()
        print(d.get_pose().position[:4])

    def right():
        x, y, z, r = d.get_pose().position[0:4]
        d.movej(x,y-10,z,r)
        d.clear_alarms()
        print(d.get_pose().position[:4])
    
    def forward():
        x, y, z, r = d.get_pose().position[0:4]
        d.movej(x+10,y,z,r)
        d.clear_alarms()
        print(d.get_pose().position[:4])

    def back():
        x, y, z, r = d.get_pose().position[0:4]
        d.movej(x-10,y,z,r)
        d.clear_alarms()
        print(d.get_pose().position[:4])

    def up():
        x, y, z, r = d.get_pose().position[0:4]
        d.movej(x,y,z+10,r)
        d.clear_alarms()
        print(d.get_pose().position[:4])

    def down():
        x, y, z, r = d.get_pose().position[0:4]
        d.movej(x,y,z-10,r)
        d.clear_alarms()
        print(d.get_pose().position[:4])
    
    def r_L():
        x, y, z, r = d.get_pose().position[0:4]
        d.movej(x,y,z,r+10)
        d.clear_alarms()
        print(d.get_pose().position[:4])

    def r_R():
        x, y, z, r = d.get_pose().position[0:4]
        d.movej(x,y,z,r-10)
        d.clear_alarms()
        print(d.get_pose().position[:4])
    
    def suck():
        global end
        global s
        if end == 0:
            s = not s 
            d.suck(s)
            time.sleep(0.5)
    
    if index == 0: #A
        left()
    elif index == 1: #B
        down()
    elif index == 2: #C
        right()
    # elif index == 3: #I
    #     forward()
    # elif index == 4: #L
    #     back()
    elif index == 5: #U
        up()


# Define a function to handle actions for each recognized prediction
def handle_prediction(index):
    # letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letters = "ABCILU"
    control_dobot()
    if 0 <= index < 26:
        # Do something when gesture for the letter at the given index is recognized
        print(f"Gesture {letters[index]} recognized!")
    




while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x,y,w,h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255
        imgCrop = img[y-offset:y+offset+h, x-offset:x+w+offset] 


        aspectRatio = h/w

        if aspectRatio >1:
            k = imgSize/h
            wCal = math.ceil(k*w)
            imgResize = cv2.resize(imgCrop,(wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize-wCal)/2)
            imgWhite[:, wGap:wCal+wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite)
            # print(prediction, index)
            handle_prediction(index)
            
        else:
            k = imgSize/w
            hCal = math.ceil(k*h)
            imgResize = cv2.resize(imgCrop,(imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize-hCal)/2)
            imgWhite[hGap:hCal+hGap, :] = imgResize
            prediction, index = classifier.getPrediction(imgWhite)
            handle_prediction(index)
            # print(prediction, index)

        cv2.rectangle(imgOutput, (x-offset, y-offset-50), (x-offset+150, y-offset-50+50), (255,0,255), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x,y-20), cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255), 2)
        cv2.rectangle(imgOutput, (x-offset,y-offset), (x+w+offset, y+h+offset), (255,0,255), 4)

    cv2.imshow("Image", imgOutput)
    key = cv2.waitKey(500)
    if key == 27:
        break

