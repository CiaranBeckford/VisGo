from __future__ import print_function
from algo import agent
from algo import goboard
from algo import gotypes
from algo.utils import print_board, print_move, init_location
import time
import cv2


def main():
    img = cv2.imread('algo/gameboard.png')
    matrix = init_location()
    board_size = 9
    game = goboard.GameState.new_game(board_size)
    bots = {
        gotypes.Player.black: agent.RandomBot(),
        gotypes.Player.white: agent.RandomBot(),
    }
    while not game.is_over():
        time.sleep(0.3)

        print(chr(27) + "[2J")
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move, matrix, img)
        game = game.apply_move(game.next_player, bot_move)


if __name__ == '__main__':
    main()
