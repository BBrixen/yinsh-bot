from utils import convert_coord_to_output, convert_input_to_coord
from gameplay_mechanics import remove_line, valid_moves_for_ring
color_to_int = {'white': 1, 'black': 2}
int_to_color = {1: 'white', 2: 'black'}

def prompt_remove_line(board, lines):
    print(f"pick a line of 5 to remove")
    for i, line in enumerate(lines):
        print(f"{i}: {convert_coord_to_output(line[0])}-{convert_coord_to_output(line[-1])}")
    try:
        line_num = int(input())
    except ValueError:
        line_num = 0

    line = lines[line_num]
    remove_line(board, line, False)


def prompt_remove_ring(rings):
    print("Choose a ring to remove")
    rings = list(rings)
    for i, ring in enumerate(rings):
        print(f"{i}: {convert_coord_to_output(ring)}")
    try:
        ring_num = int(input())
    except ValueError:
        ring_num = 0
    return rings[ring_num]


def get_user_move(board, color):
    while True:
        try:
            print(f"{int_to_color[color]}: input your move in the form 'x10-z12'")
            str_move = input().strip().split('-')
            if len(str_move) != 2:
                continue

            start, end = str_move[0], str_move[1]
            start = convert_input_to_coord(start)
            end = convert_input_to_coord(end)
            move = (start, end)

            rings = board.white_rings
            if color == 2:
                rings = board.black_rings

            if start not in rings:
                print("not valid start")
                continue
        except ValueError:
            continue

        moves = valid_moves_for_ring(board, start)
        if move not in moves:
            print("not in end locations")
            continue

        move = (start, end)
        return move