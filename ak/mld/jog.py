import time
import pydobot
from serial.tools import list_ports
from pynput import keyboard
from pynput.keyboard import Key


available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[-1].device
d = pydobot.Dobot(port)
# d.suck(False)
d.speed()
end = 0
s = False
x, y, z, r = d.get_pose().position[0:4]
print(x, y, z, r)


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
    
    def suck():
        global end
        global s
        if end == 0:
            s = not s 
            d.suck(s)
            time.sleep(0.5)
            

    def on_press(key):
        global end
        try:
            if key == keyboard.KeyCode.from_char('w'):
                forward()
            elif key == keyboard.KeyCode.from_char('s'):
                back()
            elif key == keyboard.KeyCode.from_char('d'):
                left()
            elif key == keyboard.KeyCode.from_char('a'):
                right()
            elif key == keyboard.Key.space:
                suck()
            elif key == keyboard.KeyCode.from_char('i'):
                up()
            elif key == keyboard.KeyCode.from_char('k'):
                down()
            elif key == keyboard.KeyCode.from_char('j'):
                r_L()
            elif key == keyboard.KeyCode.from_char('l'):
                r_R()
        except KeyboardInterrupt:
            pass

    # Listen for key presses
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == '__main__':
    control_dobot()


        



        