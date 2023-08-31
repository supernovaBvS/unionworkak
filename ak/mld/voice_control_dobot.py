import speech_recognition as sr
import pyttsx3
import cv2
import random
import time
import numpy as np
import pydobot
from serial.tools import list_ports

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[-1].device

d = pydobot.Dobot(port)
print('start')

recognizer = sr.Recognizer()
microphone = sr.Microphone()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Use the default microphone as the audio source
def listen():
    with microphone as source:
        print("Say something!")
        audio = recognizer.listen(source)
        
        try:
            # Use the PocketSphinx engine for local speech recognition
            text = recognizer.recognize_sphinx(audio)
            print("You said:", text)
            return text.lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print("Error with the request; {0}".format(e))
            return None

def control_dobot():

    def left():
        x, y, z, r = d.get_pose().position[0:4]
        d.movej(x,y-10,z,r)
        print(d.get_pose().position[:4])

    def right():
        x, y, z, r = d.get_pose().position[0:4]
        d.movej(x,y+10,z,r)
        print(d.get_pose().position[:4])
    
    def forward():
        x, y, z, r = d.get_pose().position[0:4]
        d.movej(x+10,y,z,r)
        print(d.get_pose().position[:4])

    def back():
        x, y, z, r = d.get_pose().position[0:4]
        d.movej(x-10,y,z,r)
        print(d.get_pose().position[:4])

    def up():
        x, y, z, r = d.get_pose().position[0:4]
        d.movej(x,y,z+10,r)
        print(d.get_pose().position[:4])

    def down():
        x, y, z, r = d.get_pose().position[0:4]
        d.movej(x,y,z-10,r)
        print(d.get_pose().position[:4])
    
    def r_L():
        x, y, z, r = d.get_pose().position[0:4]
        d.movej(x,y,z,r+10)
        print(d.get_pose().position[:4])

    def r_R():
        x, y, z, r = d.get_pose().position[0:4]
        d.movej(x,y,z,r-10)
        print(d.get_pose().position[:4])

    while True:
        command = listen()

        if command is None:
            continue

        if 'up' in command:
            up()
        if 'down' in command:
            down()
        if 'left' in command:
            left()
        if 'right' in command:
            right()
        if 'forward' in command:
            forward()
        if 'back' in command:
            back()
        if 'twist' and 'left' in command:
            r_L()
        if 'twist' and 'right' in command:
            r_R()
        if 'break' in command:
            break


if __name__ == '__main__':
    control_dobot()

