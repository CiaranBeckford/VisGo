import cv2
from algo import agent
from algo import goboard
from algo import gotypes
from algo.utils import print_board, print_move, point_from_coords, init_location, init_axes
from six.moves import input


def main():
    board_size = 9
    game = goboard.GameState.new_game(board_size)
    bot = agent.RandomBot()
    img = cv2.imread('algo/gamebooard.png')
    img = init_axes(img)
    game_state_img = img_w_coords = img
    matrix = init_location()
    while not game.is_over():
        print(chr(27) + "[2J")
        print_board(game.board)
        cv2.imshow("VisGo", img_w_coords)
        cv2.waitKey(1000)
        if game.next_player == gotypes.Player.black:
            human_move = input('-- ')
            point = point_from_coords(human_move.strip())
            move = goboard.Move.play(point)
        else:
            move = bot.select_move(game)
        img_w_coords, game_state_img = print_move(game.next_player, move, matrix, game_state_img)
        game = game.apply_move(game.next_player, move)
if __name__ == '__main__':
    main()
