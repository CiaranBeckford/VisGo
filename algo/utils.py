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
    print(coords)
    print(move_str)
    img_w_coords, game_state_img = display_move(player,img, coords, matrix)
    return (img_w_coords, game_state_img)


def print_board(board):
    for row in range(board.num_rows, 0, -1):
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(gotypes.Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print('%d %s' % (row, ''.join(line)))
    print('  ' + COLS[:board.num_cols])

def display_move(player, img, coords, matrix):
    inv_map = {v: k for k, v in matrix.items()}
    game_state_img = None
    if player == player.white:
        game_state_img = (cv2.circle(img, coords, 20, (255, 255, 255), - 1)).copy()
        img_w_coords = cv2.putText(img, str(inv_map[coords]), (520,30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    else:
        game_state_img = (cv2.circle(img, coords, 20, (0, 0, 0), - 1)).copy()
        img_w_coords = cv2.putText(img, str(inv_map[coords]), (270,30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    return (img_w_coords, game_state_img)

def init_location():
    alpha_num = []
    cols = "ABCDEFGHI"
    rows = [1,2,3,4,5,6,7,8,9]

    for i in cols:
        for j in rows:
            temp = i+str(j)
            alpha_num.append(temp)
    alpha_num
    x= y = [x for x in range(72,510,54)]
    real_coords = list()
    for i in x:
        for j in y:
            real_coords.append((i,j))
    col_start = 8
    count = 1
    inc = 8
    intersection_dict = dict()
    for alpha in alpha_num:
        if count % 10 == 0:
            inc+=9
            count = 1
            col_start = inc
        intersection_dict.update({alpha : real_coords[col_start]})
        col_start-=1
        count+=1
    return (intersection_dict)

def point_from_coords(coords):
    col = COLS.index(coords[0]) + 1
    row = int(coords[1:])
    return gotypes.Point(row=row, col=col)

def init_axes(img):
    '''borderType = cv2.BORDER_CONSTANT
    top = int(0.1 * img.shape[0])  # shape[0] = rows
    bottom = top
    left = int(0.1 * img.shape[1])  # shape[1] = cols
    right = left
    value = (109, 176, 242)
    dst = cv2.copyMakeBorder(img, top, bottom, left, right, borderType, None, value)
    dst = cv2.imwrite("board_3.png", dst)'''

    count = 80
    cols = "ABCDEFGHI"
    for row in range(9,0,-1):
        img = cv2.putText(img, str(row), (20,count),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        count+=54
    count = 68
    for col in cols:
        img = cv2.putText(img, str(col), (count,560),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        count+=55

    img = cv2.putText(img, "(BOT MOVE) - white: ", (350,30),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    img = cv2.putText(img, "(PLAYER MOVE) - black: ", (72,30),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    return img
