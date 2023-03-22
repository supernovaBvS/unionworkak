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

    def capture_checkerboard(self):
        d.movej(self.home[0], self.home[1], self.home[2], 0)
        self.frame = self.cap.read()[1]
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.frame = cv2.GaussianBlur(self.frame, (5, 5), 0)
        _, self.frame = cv2.threshold(self.frame, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(self.frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]
        squares = []
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02*peri, True)
            if len(approx) == 4 and cv2.contourArea(c) > 10000:
                squares.append(approx)
        squares = sorted(squares, key=cv2.contourArea, reverse=True)[:1]
        self.boardcnt = squares[0].reshape(4, 2)
        self.checkerboard = self.get_checkerboard()  # get the checkerboard in array format

    def compare_checkerboards(self):  # compare new and old checkerboard
        if (sum(map(lambda c0, c1, c2: c0 == c1 == c2,
                    self.checkerboardchecks[0], self.checkerboardchecks[1],
                    self.checkerboardchecks[2])) == 9):  # 3 same check results of new
            different = sum(map(lambda c, c0: c != c0, self.checkerboard,
                                self.checkerboardchecks[0]))  # difference of old and new
            if different == 1:
                if (
                    sum([not int(x) for x in self.checkerboard if x == '0']
                        ) - sum([not int(x) for x in self.checkerboardchecks[0]
                                if x == '0']) == 1):  # grid with chess different count = -1
                    return True
                else:
                    return False
            elif different == 0:
                return False
            else:
                pass
        else:
            return False
    
    def find_contour(self, src, lmask, umask, lmask1=0, umask1=0, get_center=False):
        blurred = cv2.GaussianBlur(src, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lmask, umask)
        if lmask1 + umask1 is not 0:
            mask1 = cv2.inRange(hsv, lmask1, umask1)
            mask = cv2.bitwise_or(mask, mask1)
        
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)  # only return the contour with max area
            area = cv2.contourArea(contour)
            
            if get_center:
                moments = cv2.moments(contour)
                if moments['m00'] != 0:
                    cX = int(moments['m10'] / moments['m00'])
                    cY = int(moments['m01'] / moments['m00'])
                else:
                    cX, cY = (self.cx, self.cy)
                    
                return contour, area, (cX, cY)
            else:
                return contour, area
        else:
            if get_center:
                return 0, 0, (False, False)
            else:
                return 0, 0
            
    def cntcenter(self, src, threshold, lmask, umask, lmask1=0, umask1=0):
        """
        Find contours of all placed chess and get their centers.

        Args:
        - src: Source image
        - threshold: Minimum area threshold for a contour to be considered
        - lmask, umask: Lower and upper HSV color masks
        - lmask1, umask1: Additional lower and upper HSV color masks (optional)
        
        Returns:
        - centers: List of tuples representing the centers of the contours
        """
        blurred = cv2.GaussianBlur(src, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lmask, umask)
        if lmask1 + umask1 is not 0:
            mask1 = cv2.inRange(hsv, lmask1, umask1)
            mask = cv2.bitwise_or(mask, mask1)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        centers = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < threshold:
                continue
            Moments = cv2.moments(contour)
            cX = int(Moments['m10'] / Moments['m00'])
            cY = int(Moments['m01'] / Moments['m00'])
            center = (cX, cY)
            centers.append(center)
            
        return centers
    
    def transform(self):  
        global pts1
        contour, area = self.cnt(self.frame, np.array([0, 0, 0]),
                                np.array([255,150,75]))
        img2 = self.frame
        edges = cv2.drawContours(img2, contour, -1, (0, 255, 0), 1)
        cv2.imshow("contours", img2)

        print('board area = ', area)
        if area < 10000:
            return False

        epsilon = 0.05*cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        print(approx)

        if not hasattr(self, "pts1"):
            self.pts1 = np.float32(approx)

        pts2 = np.float32([[0, 0], [0, 300], [300, 300], [300, 0]])
        M = cv2.getPerspectiveTransform(self.pts1, pts2)
        self.frame = cv2.warpPerspective(self.frame, M, (300, 300))

        self.grids = []
        for i in range(9):
            x1, x2 = self.grid[0, i // 3], self.grid[0, i // 3 + 1]
            y1, y2 = self.grid[1, i % 3], self.grid[1, i % 3 + 1]
            self.grids.append(self.frame[x1:x2, y1:y2])

        return True
    
    # def cntcenter(self, img, area_thresh, *args):
    #     img = cv2.GaussianBlur(img, (5, 5), 0)
    #     centers = []
    #     for lower, upper in args:
    #         mask = cv2.inRange(img, lower, upper)
    #         _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE,
    #                                         cv2.CHAIN_APPROX_SIMPLE)
    #         for cnt in contours:
    #             area = cv2.contourArea(cnt)
    #             if area > area_thresh:
    #                 moments = cv2.moments(cnt)
    #                 center = (int(moments["m10"] / moments["m00"]),
    #                         int(moments["m01"] / moments["m00"]))
    #                 centers.append(center)
    #     return centers


    def recognize_squares(self, gn, lower, upper):
        contour, area = self.cnt(gn, lower, upper)
        if area > self.b_value:
            return 2
        contour, area = self.cnt(gn, *lower[1:], *upper[1:])
        if area > self.r_value:
            return 1
        return 0


    def check(self, delay=0, startc=0, getCenter=0):
        try:
            _, _, self.frame = self.camera.capture()
            if self.transform():
                return False
        except cv2.error:
            print('camera blocked')
            return False

        if getCenter:
            blue_centers = self.cntcenter(
                self.frame, self.b_value, ((80, 100, 50), (120, 255, 255)))
            red_centers = self.cntcenter(
                self.frame, self.r_value, ((0, 100, 90), (10, 255, 255)), ((170, 100, 90), (180, 255, 255)))
            print(blue_centers, '\n', red_centers)
            return blue_centers, red_centers

        squares = [self.recognize_squares(
            gn, ((80, 100, 50), (120, 255, 255)), ((0, 100, 90), (10, 255, 255), (170, 100, 90), (180, 255, 255))) for gn in self.grids]

        print('squares = ', squares)
        checking = [str(square) for square in squares]
        print('checking = ', checking)

        if startc and checking == ['0'] * 9:
            return True

        if '3' in checking:
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
            #     if np.count_nonzero(rn[0] == 2) == 3:  # lose
            #         self.sit = 7
            #         return self.sit
            #     elif np.count_nonzero(rn[0] == 1) == 3:  # win
            #         self.sit = 8
            #         return self.sit
            # if np.count_nonzero(self.checkerboardv) == 9:  # draw
            #     self.sit = 6
            #     return self.sit
                if np.count_nonzero(rn[0] == 2) == 3:
                    return self.SITUATION_LOSE

                if np.count_nonzero(rn[0] == 1) == 3:
                    return self.SITUATION_WIN

            if np.count_nonzero(self.checkerboardv) == 9:
                return self.SITUATION_DRAW


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
            elif self.sit == 8:
                print('You win!')
            elif self.sit == 7:
                print('You lose!')
            elif self.sit == 6:
                print('Draw!')

            for checker_color, centers in ((1, self.red_centers), (2, self.blue_centers)):
                for i, center in enumerate(centers):
                    x, y = self.x + (center[1] - self.cx), self.y + (center[0] - self.cy)

                    # Pick up checker
                    d.suck(False)
                    d.jump(x, y, self.z, 0)
                    d.suck(True)
                    time.sleep(1)

                    # Place checker in corresponding position
                    if checker_color == 1:
                        j = i
                    else:
                        j = -1
                    pos_x, pos_y = self.pos[j][0], self.pos[j][1]
                    d.jump(pos_x, pos_y, self.z, 0)
                    d.suck(False)

            # Clear checkerboard and game variables
            self.reset_game()

            # Prompt user to play again or exit
            play_again = input("Do you want to play again? (y/n)").lower() == "y"
            if play_again:
                self.start()
            else:
                print("Thanks for playing!")

def main():
    game = CheckersGame()
    game.start()
    while True:
        game.check()
        play_again = input("Do you want to play again? (y/n)").lower() == "y"
        if play_again:
            game.reset_game()
        else:
            break

if __name__ == '__main__':
    main()



