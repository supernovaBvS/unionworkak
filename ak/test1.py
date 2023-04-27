import cv2
import random
import time
import numpy as np
import pydobot
from serial.tools import list_ports

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[3].device

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



class Checkergame:
    def __init__(
        self, test=0, z=-50, x=300 , y=41, x_offset=-45, y_offset=-45,
        home=[200, -140, 0], first=1, r_value=1500, b_value=1500, upr=0.0,
            cx=150, cy=150, SITUATION_LOSE = 7, SITUATION_WIN = 8, SITUATION_DRAW = 6
            ):
        self.test = test
        self.r_value = r_value  # color area threshold
        self.b_value = b_value  # ''
        self.SITUATION_LOSE = SITUATION_LOSE
        self.SITUATION_WIN = SITUATION_WIN
        self.SITUATION_DRAW = SITUATION_DRAW

        self.round = 0  # moved count
        self.first = first  # is bot first
        self.blankcount = 0
        self.x, self.y, self.z = x, y, z  # grid #1 coordinates (top left of Dobot #1)

        self.upr = upr  # unit pixel ratio
        self.cx, self.cy = cx, cy  # grid #1 center image coordinates (normally (55, 55))
        self.x_offset, self.y_offset = x_offset, y_offset
        self.xupr, self.yupr = self.x_offset , self.y_offset   # unit pixel ratio
        self.cap = cv2.VideoCapture(0)
        self.home = home  # home position
        self.sit = 0  # situation id
        self.pos = [(self.x+2, self.y+self.y_offset*2-35),
                    (self.x+self.x_offset, self.y+self.y_offset*2-35),
                    (self.x+2*x_offset, self.y+self.y_offset*2-35),
                    (self.x, self.y+43),
                    (self.x+self.x_offset, self.y+43),
                    (self.x+2*self.x_offset, self.y+40)]  # default chess coordinates
        print (self.pos)
        self.checkattemp = 0  # saving checks
        self.checkerboardchecks = ['0' * 9] * 3  # list of self.checkattemp
        self.checkerboard = '0' * 9  # checkerboard with color id
        self.grid = np.array([[0, 100, 200, 300], [0, 100, 200, 300]])  # cropping

    def c(self):
        """Capture the checkerboard."""
        d.movej(self.home[0], self.home[1], self.home[2], 0)
        self.frame = self.cap.read()[1]

    def com(self):
        """Compare new and old checkerboard."""
        # Check if the last 3 checkerboard captures are the same
        if all(x == self.checkerboardchecks[0] for x in self.checkerboardchecks[1:]):
            # Count the number of different checkerboard squares
            different = sum(c1 != c2 for c1, c2 in zip(self.checkerboard, self.checkerboardchecks[0]))
            # Check if only one square is different
            if different == 1:
                # Check if the difference is in the chess grid
                if self.checkerboard.count('0') == self.checkerboardchecks[0].count('0') + 1:
                    return True  # Chess has been moved
        return False

    def cnt(self, src, lmask, umask, lmask1=0, umask1=0, getCenter=False):
        blurred = cv2.GaussianBlur(src, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lmask, umask)
        if np.any(lmask1 + umask1):
            mask1 = cv2.inRange(hsv, lmask1, umask1)
            mask += mask1
        
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)  # only return the contour with max area
            area = cv2.contourArea(contour)
            if getCenter:
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
            if getCenter:
                return 0, 0, (False, False)
            else:
                return 0, 0

    def cntcenter(self, src, threshold, lmask, umask, lmask1=0, umask1=0):
        blurred = cv2.GaussianBlur(src, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lmask, umask)
        if np.any(lmask1 + umask1):
            mask1 = cv2.inRange(hsv, lmask1, umask1)
            mask += mask1
        
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        self.centers = []
        if len(contours) > 0:
            for contour in contours:
                if cv2.contourArea(contour) < threshold:
                    continue
                else:
                    Moments = cv2.moments(contour)
                    cX = int(Moments['m10'] / Moments['m00'])
                    cY = int(Moments['m01'] / Moments['m00'])
                    center = (cX, cY)
                    self.centers.append(center)
        return self.centers

    def transform(self):  # matrix perspective transform of image
        global initstat, pts1
        contour, area = self.cnt(self.frame, np.array([0, 0, 0]),
                                 np.array([255,150,75])) #255,150,75
        img2= self.frame
        edges=cv2.drawContours(img2, contour, -1, (0,255,0), 1)
        cv2.imshow("contours", img2)
        
        print('board area = ', area)
        if area < 10000:
            return True
            pass
        
        epsilon = 0.05*cv2.arcLength(contour, True)
        
        approx = cv2.approxPolyDP(contour, epsilon, True)
        print(approx)
        if initstat or True:
            pts1 = np.float32(approx)
            initstat = False
        pts2 = np.float32([[0, 0], [0, 300], [300, 300], [300, 0]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        self.frame = cv2.warpPerspective(self.frame, M, (300, 300))

        self.grids = []
        for i in range(9):
            self.grids.append(
                self.frame[self.grid[0, i // 3]:self.grid[0, i // 3+1],
                           self.grid[1, i % 3]:self.grid[1, i % 3+1]])
            
    def check(self, delay=0, startc=0, getCenter=0):  # recognize the checkerboard
        global initstat
        self.c()
        try:
            if self.transform():
                return False
        except cv2.error:
            initstat = True
            print('camera blocked')
            return False

        self.centers = {}
        self.checkattemp += 1
        checking = ''
        print('red area    blue area')
        for gn, i in zip(self.grids, range(9)):
            # blue
            lower_blue = np.array([80, 100, 50]) #'''90, 100, 90'''
            upper_blue = np.array([120, 255, 255])#110,255,255
            # red
            lower_red = np.array([0, 100, 90])#0, 100, 100
            upper_red = np.array([10, 255, 255])#
            lower_red1 = np.array([170, 100, 90])
            upper_red1 = np.array([180, 255, 255])

            if getCenter:
                self.blue_centers = self.cntcenter(
                    self.frame, self.b_value, lower_blue, upper_blue)

                self.red_centers = self.cntcenter(
                    self.frame, self.r_value, lower_red, upper_red, lower_red1, upper_red1 )

                print(self.blue_centers, '\n', self.red_centers)
                return self.blue_centers, self.red_centers
            else:
                contour_blue, area_blue = self.cnt(gn, lower_blue, upper_blue)
                contour_red, area_red = self.cnt(
                    gn, lower_red, upper_red, lower_red1, upper_red1)
                #print(area_red, area_blue, sep='  ')

            if area_red > self.r_value and area_blue < self.b_value:
                checking += '1'
            elif area_red < self.r_value and area_blue > self.b_value:
                checking += '2'
            elif area_red < self.r_value and area_blue < self.b_value:
                checking += '0'
            else:
                checking += '3'

        print('checking = ', checking)
        if startc:
            if checking == '000000000':
                return True
        self.checkerboardv = np.array(
            [int(x) for x in self.checkerboard]).reshape(3, 3)
        if '3' in checking:
            return False
        if checking == '000000000' and self.first == 1 and self.round == 0:
            self.checkerboard = checking
            return True
        else:
            self.checkerboardchecks[self.checkattemp % 3] = checking
        if checking == '000000000':
            if self.checkerboard != '000000000':
                self.blankcount += 1
        else:
            self.blankcount = 0
        if self.com():
            self.checkerboard = checking
            return True
        else:
            return False

    def rows(self):  # divide the checkerboard into 8 rows
        self.checkerboardv = np.array(
            [int(x) for x in self.checkerboard]).reshape(3, 3)
        self.r = list()
        self.r.append((self.checkerboardv[0], 0))
        self.r.append((self.checkerboardv[1], 1))
        self.r.append((self.checkerboardv[2], 2))
        self.r.append((self.checkerboardv[:, 0], 3))
        self.r.append((self.checkerboardv[:, 1], 4))
        self.r.append((self.checkerboardv[:, 2], 5))
        self.r.append((self.checkerboardv.diagonal(), 6))
        self.r.append((np.flip(self.checkerboardv, 1).diagonal(), 7))

    def situation(self):
        self.sit = 0
        self.rows()
        for rn in self.r:
            if np.count_nonzero(rn[0] == 2) == 3:
                self.sit = 7
                return self.sit

            if np.count_nonzero(rn[0] == 1) == 3:
                self.sit = 8
                return self.sit

        if np.count_nonzero(self.checkerboardv) == 9:
            self.sit = 6
            return self.sit


        if self.sit == 0:
            for rn in self.r:
                if np.count_nonzero(rn[0] == 0):  # 0xx
                    self.sit = 0
                    self.move = [rn[1], int(np.where(rn[0] == 0)[0][0])]
                else:
                    pass

        for rn in self.r:
            if (np.count_nonzero(
                rn[0] == 2) == 2 and np.count_nonzero(
                    rn[0] == 0) == 1):  # 220
                self.sit = 1
                self.move = [rn[1], int(np.where(rn[0] == 0)[0][0])]
                break

        for rn in self.r:
            if (np.count_nonzero(
                rn[0] == 0) == 1 and np.count_nonzero(
                    rn[0] == 1) == 2):  # 110
                self.sit = 2
                self.move = [rn[1], int(np.where(rn[0] == 0)[0][0])]
                break

        if self.checkerboard in movex:
            self.move = random.choice(movex[self.checkerboard])
            self.move = [self.move // 3, self.move % 3]
        else:
            if self.move[0] in range(0, 3):
                pass
            elif self.move[0] in range(3, 6):
                self.move = [self.move[1], self.move[0] - 3]
            elif self.move[0] == 6:
                self.move = [self.move[1], self.move[1]]
            elif self.move[0] == 7:
                self.move = [self.move[1], 2 - self.move[1]]

        return self.sit

    def intention(self):
        self.coor = [self.x + self.x_offset * self.move[0],
                    self.y + self.y_offset * self.move[1]]
        print(f"Intended move: {self.move}")
        print(f"Coordinates: {self.coor}")
        return self.coor


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
        d.jump(self.home[0], self.home[1], self.home[2], 0)

        self.checkerboard = self.checkerboard[
            :self.move[0] * 3 + self.move[1]] + '1' + self.checkerboard[
            self.move[0] * 3 + self.move[1] + 1:]
        self.round += 1

    def start(self):
        while True:
            user_choice = input("Do you want to go first? (y/n) ").lower()
            if user_choice == 'y':
                self.first = False
                print('You go first.')
                return 'Game Start'
            elif user_choice == 'n':
                self.first = True
                print('Bot goes first.')
                return 'Game Start'
            else:
                print('please clear the board.')
                print("Invalid input. Please enter 'y' or 'n'.")
            time.sleep(1.5)

    def reset_game(self):
        self.first = True if self.sit == 9 else not self.first
        self.sit = 0
        self.checkerboardv, self.checkerboard = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]), '0' * 9
        self.checkerboardchecks = ['0' * 9] * 3
        self.checkattemp = 0
        self.round = 0
        self.blankcount = 0

    def end(self):
        if self.sit < 5:
            pass
        else:
            while self.check(getCenter=True) is False:
                pass
            self.reds = np.where(self.checkerboardv.reshape(9) == 1)[0]
            self.blues = np.where(self.checkerboardv.reshape(9) == 2)[0]

            if self.sit == 9:
                print('Game interrupted')
            elif self.sit == self.SITUATION_WIN:
                print('You win!')
            elif self.sit == self.SITUATION_LOSE:
                print('You lose!')
            elif self.sit == self.SITUATION_DRAW:
                print('Draw!')

            # for checker_color, centers in ((1, self.red_centers), (2, self.blue_centers)):
            #     for i, center in enumerate(centers):
            #         x, y = self.x + (center[1] - self.cx), self.y + (center[0] - self.cy)

            #         # Pick up checker
            #         d.suck(False)
            #         d.jump(x, y, self.z, 0)
            #         d.suck(True)
            #         d.movej(x, y, self.z+40, 0)
            #         time.sleep(1)

            #         # Place checker in corresponding position
            #         if checker_color == 1:
            #             j = i
            #         else:
            #             j = -1
            #         pos_x, pos_y = self.pos[j][0], self.pos[j][1]
            #         d.jump(pos_x, pos_y, self.z, 0)
            #         d.suck(False)

            for i, j in zip(self.red_centers, range(len(self.red_centers))):  # red
                # get
                self.coor = [self.x + (i[1] - self.cx),
                             self.y + (i[0] - self.cy)]

                d.suck(False)
                d.jump(self.coor[0], self.coor[1], self.z, 0)
                d.suck(True)
                time.sleep(1)

                # place
                d.jump(self.pos[j][0], self.pos[j][1], self.z, 0)
                d.suck(False)

            for i, j in zip(self.blue_centers, range(len(self.blue_centers))):  # blue
                # get
                self.coor = [self.x + (i[1] - self.cx),
                             self.y + (i[0] - self.cy)]

                d.suck(False)
                d.jump(self.coor[0], self.coor[1], self.z, 0)
                d.suck(True)
                time.sleep(1)

                # place
                d.jump(self.pos[-1][0], self.pos[-1][1], self.z, 0)

                d.suck(False)

            d.movej(self.pos[-1][0], self.pos[-1][1], self.z + 20, 0)
            d.movej(self.home[0], self.home[1], self.home[2], 0)
            self.first = True if self.sit == 9 else not self.first
            self.sit == 0
            self.checkerboardv, self.checkerboard = np.array(
                [[0, 0, 0], [0, 0, 0], [0, 0, 0]]), '0' * 9

            self.start()
            self.checkerboard = '0' * 9
            self.checkerboardchecks = ['0' * 9] * 3
            self.checkattemp = 0
            self.round = 0
            self.blankcount = 0


# main
def main():
    global board
    board = Checkergame(1)
    board.start()


    while True:
        print(board.checkerboard)
        try:
            if board.round % 2 != board.first or True:  # turn
                if board.check():
                    # cv2.imshow('frame', board.frame)
                    #board.intention()

                    if board.situation() < 5 :
                        board.intention()
                        board.m()
                        time.sleep(6)
                    elif board.sit > 5:
                        board.end()
                        time.sleep(5 + board.round * 10)
                else:
                    pass
                if board.blankcount >= 10:
                    board.sit = 9
                    board.end()

        except KeyboardInterrupt:
            return None


if __name__ == '__main__':
    initstat = True
    main()
    pass