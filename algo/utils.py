from . import gotypes
import cv2
import numpy as np

COLS = 'ABCDEFGHIJKLMNOPQRST'
STONE_TO_CHAR = {
    None: '.',
    gotypes.Player.black: 'x',
    gotypes.Player.white: 'o',
}

def print_move(player, move, matrix, img):
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = '%s%d' % (COLS[move.point.col - 1], move.point.row)
    print('%s %s' % (player, move_str))
    coords = matrix[move_str]
    display_move(player,img, coords)


def print_board(board):
    for row in range(board.num_rows, 0, -1):
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(gotypes.Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print('%d %s' % (row, ''.join(line)))
    print('  ' + COLS[:board.num_cols])

def display_move(player, img, coords):
    if player == player.white:
        image = cv2.circle(img, coords, 20, (255, 255, 255), - 1)
    else:
        image = cv2.circle(img, coords, 20, (0, 0, 0), - 1)
    cv2.imshow("", image)
    cv2.waitKey(2)

def init_location():
    alpha_num = []
    cols = "ABCDEFGHI"
    rows = [1,2,3,4,5,6,7,8,9]

    for i in cols:
        for j in rows:
            temp = i+str(j)
            alpha_num.append(temp)
    alpha_num
    x= y = [x for x in range(32,468,54)]

    real_coords = list()
    for i in x:
        for j in y:
            real_coords.append((i,j))
    col_start = 8
    count = 1
    dec = 8
    intersection_dict = dict()
    for alpha in alpha_num:
        if count % 10 == 0:
            dec-=1
            count = 1
            col_start = dec
        intersection_dict.update({alpha : real_coords[col_start]})
        col_start+=9
        count+=1
    return (intersection_dict)
