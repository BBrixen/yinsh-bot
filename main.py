from gameplay_mechanics import Board, place_ring, apply_move, rings_to_place, valid_moves, create_grid_from_file
from utils import convert_input_to_coord, convert_coord_to_output, flip_player
from user_input import int_to_color, get_user_move
from bot_input import get_bot_move
from utils import max_dimension
from random import randint

import cProfile
import pstats


def play_human_to_human():
    board = Board()
    create_grid_from_file(board)

    cur_player = 1
    while len(board.white_rings) < rings_to_place or len(board.black_rings) < rings_to_place:
        print(board)

        valid = False
        while not valid:
            print(f"{int_to_color[cur_player]} enter a coordinate for a ring")
            try:
                coord = convert_input_to_coord(input())
            except ValueError:
                valid = False
                continue

            valid = place_ring(board, cur_player, coord)

        cur_player = flip_player(cur_player)

    # rings places, main game loop
    cur_player = 2
    while board.winner == 0:
        print(board)

        move = get_user_move(board, cur_player)
        board = apply_move(board, move, cur_player, False)
        if cur_player == 1:
            cur_player = 2
        else:
            cur_player = 1

    print(f"the winner is {int_to_color[board.winner]}")


def play_human_to_bot():
    board = Board()
    create_grid_from_file(board)

    cur_player = 1
    starting_valid_moves = -1

    while len(board.white_rings) < rings_to_place or len(board.white_rings) < rings_to_place:
        print(board)
        valid = False
        coord = None, None

        while not valid:
            print(f"{int_to_color[cur_player]} enter a coordinate for a ring")
            try:
                coord = convert_input_to_coord(input())
            except ValueError:
                valid = False
                continue

            valid = place_ring(board, 1, coord)
            # have the bot match opposing tiles
        x, y = coord
        coord = y, x

        bot_placed = place_ring(board,2, coord)
        while not bot_placed:
            # player placed ring on diagonal, choose random location
            x = randint(1, max_dimension-2)
            y = randint(1, max_dimension-2)
            coord = y, x
            bot_placed = place_ring(board, 2, coord)

        print(f"bot chose {convert_coord_to_output(coord)}")

    while board.winner == 0:
        print(board)

        if cur_player == 1:
            move = get_user_move(board, cur_player)
        else:
            if starting_valid_moves == -1:
                starting_valid_moves = len(valid_moves(board, cur_player))

            move = get_bot_move(board, cur_player, starting_valid_moves)
            start, end = move
            print(f"bot chose {convert_coord_to_output(start)} - {convert_coord_to_output(end)}")

        board = apply_move(board, move, cur_player, cur_player==2)
        cur_player = flip_player(cur_player)




def main():
    with cProfile.Profile() as pr:
        cProfile.run('play_human_to_bot()')

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename="bot_profiling.prof")

    # play_human_to_human()
    # play_human_to_bot()


if __name__ == '__main__':
    main()
