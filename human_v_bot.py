import cv2
import numpy as np
import threading
import time
from algo import agent
from algo import goboard
from algo import gotypes
from algo.utils import print_board, print_move, point_from_coords, init_location, init_axes
from six.moves import input
from hand_input import categorize

def get_coord(self):
    #print(self.coords)
    return self.coords
def init_overlay(self,frame):
    #cv2.line(img=frame, pt1=(72, 72), pt2=(510  , 72), color=(255, 0, 0), thickness=1, lineType=8, shift=0)
    #cv2.line(img=frame, pt1=(72, 72), pt2=(72  , 510), color=(0, 255, 0), thickness=1, lineType=8, shift=0)
    y = [x for x in range(72,505,54)]
    for num in y:
        cv2.line(img=frame, pt1=(num, 72), pt2=(num , 510), color=(0, 255, 0), thickness=1, lineType=8, shift=0)
        cv2.line(img=frame, pt1=(72, num), pt2=(510, num), color=(0, 255, 0), thickness=1, lineType=8, shift=0)
class Mythread (threading.Thread):
    def __init__(self, threadID, name, img, coords):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.img = img
        self.coords = coords
    def get_game_state_img(self,img):
        self.img = img

    def set_coords(self, coords):
        self.coords = coords
    def run(self):
        cap = cv2.VideoCapture(0)
        while(1):
            img_w_coords = self.img
            #ret, frame = cap.read()
            frame = cv2.imread("algo/One.jpg", cv2.IMREAD_UNCHANGED)
            frame_copy = cv2.imread("algo/One.jpg", cv2.IMREAD_GRAYSCALE)
            hand,coords,frame = categorize(frame, frame_copy)
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (578,578))
            self.set_coords(coords)
            init_overlay(self, frame)
            img_w_coords = np.concatenate((img_w_coords, frame), axis=1)
            cv2.imshow('frame',img_w_coords)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


def alpha_intersect(coords, inv_map):
    for i in inv_map:
        if i[0]-10<=coords[0]<=i[0]+10 and i[1]-10<=coords[1]<=i[1]+10:
            return inv_map[i]
def main():

    board_size = 9
    game = goboard.GameState.new_game(board_size)
    bot = agent.RandomBot()
    img = cv2.imread('algo/gameboard.png')
    img = init_axes(img)
    game_state_img = img_w_coords = img

    #ret, frame = cap.read()
    # Our operations on the frame come here
    #frame = cv2.flip( frame, 1)
    #frame = cv2.resize(frame, (578,578))
    matrix = init_location()
    inv_map = {v: k for k, v in matrix.items()}
    #img_w_coords = np.concatenate((img_w_coords, frame), axis=1)
    thread1 = Mythread(1, "videoThread", img_w_coords, (0,0))
    start_ = False
    thread1.start()
    while not game.is_over():
            #if start_ == False:
            thread1.get_game_state_img(img_w_coords)
            coords = get_coord(thread1)
            #print(alpha_intersect(coords,inv_map))
            #time.sleep(1)
            #print(a_row,a_col)
            print(coords)
            time.sleep(1)
            print(chr(27) + "[2J")
            print_board(game.board)
            if game.next_player == gotypes.Player.black:
                human_move = input('-- ')
                point = point_from_coords(human_move.strip())
                move = goboard.Move.play(point)
            else:
                move = bot.select_move(game)
            img_w_coords, game_state_img = print_move(game.next_player, move, matrix, game_state_img)
            game = game.apply_move(game.next_player, move)
            start_ = True
    cap.release()
    thread1.join()
if __name__ == '__main__':
    main()
