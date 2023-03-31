import speech_recognition as sr
import pyttsx3
import cv2
import random
import time
import numpy as np
import pydobot
from serial.tools import list_ports

# available_ports = list_ports.comports()
# print(f'available ports: {[x.device for x in available_ports]}')
# port = available_ports[2].device

# d = pydobot.Dobot(port)
# d.suck(False)
# d.speed()

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
print('start')

r = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Use the default microphone as the audio source
def listen():
    with sr.Microphone() as source:
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source, duration=0.2)
        
        # Listen for user input
        print("Say something!")
        speak("Say something!")
        audio = r.listen(source)
        # Recognize speech using Google Speech Recognition
        try:
            text = r.recognize_google(audio)
            print("You said: ", text)
            return text
        except:
            return None

while True:
    command = listen()

    if command is None:
        continue

    if 'coffee' in command:
        # hx, hy = pos[0]
        # d.jump(hx, hy, z+10,0)
        speak('this is your coffee')
    else:
        # hx, hy = pos[3]
        # d.jump(hx, hy, z+10,0)
        speak('this is your tea')

    # d.jump(250,0,70)
    print('end')
    break
    # d.close()