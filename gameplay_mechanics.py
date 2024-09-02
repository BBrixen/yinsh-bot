from utils import create_grid_from_file, int_to_letter, convert_coord_to_output
horizontal_starts = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 1), (6, 1), (7, 2), (8, 3), (9, 4)]
vertical_starts = [(c, r) for r,c in horizontal_starts]
diagonal_starts = [(4, 0), (3, 0), (2, 0), (1, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 1)]
row_length = 5
rings_to_place = 5
point_to_win = 3


class Board:
    def __init__(self):
        self.grid = []
        self.white_points = 0
        self.black_points = 0
        self.winner = 0
        self.black_rings = set()
        self.white_rings = set()
        self.valid_coords = set()
        self.num_white_tiles = 0
        self.num_black_tiles = 0
        self.num_black_4_rows = 0
        self.num_white_4_rows = 0
        self.num_black_3_rows = 0
        self.num_white_3_rows = 0


    def __str__(self):
        s = "    1  2  3  4  5  6  7  8  9 10 11\n"
        cur_num = 0
        for row in self.grid:
            s += f"{int_to_letter(cur_num)}  "
            cur_num += 1
            for col in row:
                if col >= 0:
                    s += " "
                s += str(col) + " "
            s += '\n'
        return s

    def __getitem__(self, item):
        row, col = item
        return self.grid[row][col]

    def __setitem__(self, key, value):
        row, col = key
        self.grid[row][col] = value

    def deep_copy(self):
        new_obj = Board()
        new_obj.grid = [row[:] for row in self.grid]
        new_obj.white_points = self.white_points
        new_obj.black_points = self.black_points
        new_obj.winner = self.winner
        new_obj.black_rings = self.black_rings.copy()
        new_obj.white_rings = self.white_rings.copy()
        new_obj.valid_coords = self.valid_coords.copy()
        new_obj.num_black_tiles = self.num_black_tiles
        new_obj.num_white_tiles = self.num_white_tiles
        new_obj.num_black_4_rows = self.num_black_4_rows
        new_obj.num_white_4_rows = self.num_white_4_rows
        new_obj.num_black_3_rows = self.num_black_3_rows
        new_obj.num_white_3_rows = self.num_white_3_rows
        return new_obj


def check_5_row(board):
    all_5_rows = []
    board.num_black_4_rows = 0
    board.num_white_4_rows = 0
    board.num_black_3_rows = 0
    board.num_white_3_rows = 0
    all_5_rows.extend(check_5_row_with_starts_and_direction(board, horizontal_starts, (0, 1)))
    all_5_rows.extend(check_5_row_with_starts_and_direction(board, vertical_starts, (1, 0)))
    all_5_rows.extend(check_5_row_with_starts_and_direction(board, diagonal_starts, (1, 1)))
    return all_5_rows

def check_5_row_with_starts_and_direction(board, starts, direction):
    all_5_rows = []
    for start in starts:
        cur_coord = start
        line = []

        while True:
            tile = board[cur_coord]
            if tile == -1:
                break  # stop searching
            if tile != 1 and tile != 2:
                line = []  # end of line

            if not line:
                line.append(cur_coord)  # add tile to empty line
            elif tile == board[line[0]]:
                line.append(cur_coord)  # add tile to current line
                check_line_length(board, line, all_5_rows, tile)
            else:
                line = [cur_coord]  # start new line of dif color

            cur_coord = cur_coord[0] + direction[0], cur_coord[1] + direction[1]
            if cur_coord not in board.valid_coords:
                break

    return all_5_rows


def check_line_length(board, line, all_5_rows, tile):
    if len(line) == row_length:
        all_5_rows.append(line[:])
        line.pop(0)
        if tile == 1:
            board.num_white_4_rows -= 1
        else:
            board.num_black_4_rows -= 1
    elif len(line) == 4:
        if tile == 1:
            board.num_white_3_rows -= 1
            board.num_white_4_rows += 1
        else:
            board.num_white_4_rows -= 1
            board.num_black_4_rows += 1
    elif len(line) == 3:
        if tile == 1:
            board.num_white_3_rows += 1
        else:
            board.num_white_4_rows += 1


def place_ring(board, color, coord):
    if coord not in board.valid_coords:
        return False

    if board[coord] != 0:
        return False

    board[coord] = color + 2
    if color == 1:
        board.white_rings.add(coord)
    else:
        board.black_rings.add(coord)
    return True


def remove_ring(board, color, coord):
    if coord not in board.valid_coords:
        return False

    if board[coord] != color+2:
        return False

    board[coord] = 0
    if color == 1:
        board.white_rings.remove(coord)
        board.white_points += 1
        if board.white_points == point_to_win:
            board.winner = color
    else:
        board.black_rings.remove(coord)
        board.black_points += 1
        if board.black_points == point_to_win:
            board.winner = color
    return True

def remove_line(board, line, bot, simulation=False):
    """line is a list of coords"""
    from user_input import prompt_remove_ring
    from bot_input import pick_ring_to_remove

    color = board[line[0]]
    for coord in line:
        board[coord] = 0

    rings = board.black_rings
    if color == 1:
        rings = board.white_rings
    if bot:
        ring_list = list(rings)
        if simulation:
            ring_num = 0
        else:
            ring_num = pick_ring_to_remove(board, ring_list)
            print(f"bot removed ring on {convert_coord_to_output(ring_list[ring_num])}")

        coord = ring_list[ring_num]
        remove_ring(board, color, coord)
    else:
        coord = prompt_remove_ring(rings)
        remove_ring(board, color, coord)


def end_points_for_ring_in_direction(board, coord, direction):
    moves = []
    cur_coord = coord
    jumping = False

    while True:
        cur_coord = cur_coord[0] + direction[0], cur_coord[1] + direction[1]

        if cur_coord not in board.valid_coords:
            return moves  # stop at edges
        if cur_coord in board.black_rings or cur_coord in board.white_rings:
            return moves  # stop at rings

        if board[cur_coord] != 0:
            jumping = True
        elif jumping:
            moves.append(cur_coord)
            return moves  # you must stop right after jumping
        else:
            moves.append(cur_coord)


def valid_moves_for_ring(board, coord):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1)]
    end_points = []
    for direction in directions:
        end_points.extend(end_points_for_ring_in_direction(board, coord, direction))

    return {(coord, e) for e in end_points}

def valid_moves(board_state, color):
    """return a set of all valid moves for a given player"""
    rings = board_state.black_rings
    if color == 1:
        rings = board_state.white_rings

    moves = set()
    for start in rings:
        ring_moves = valid_moves_for_ring(board_state, start)
        for m in ring_moves:
            moves.add(m)

    return moves


def apply_move(board, move, color, bot):
    new_board = board.deep_copy()
    if color == 1:
       apply_move_with_color(new_board, move, new_board.white_rings, color, bot)
       new_board.num_white_tiles += 1
    else:
        apply_move_with_color(new_board, move, new_board.black_rings, color, bot)
        new_board.num_black_tiles += 1

    return new_board


def apply_move_with_color(new_board, move, rings, color, bot):
    from user_input import prompt_remove_line
    from bot_input import pick_line_to_remove

    start, end = move
    rings.remove(start)
    rings.add(end)
    new_board[start] = color
    new_board[end] = color + 2

    # create normalized direction
    dirx = end[0] - start[0]
    diry = end[1] - start[1]
    if abs(dirx) >= 1:
        dirx /= abs(dirx)
        dirx = int(dirx)
    if abs(diry) >= 1:
        diry /= abs(diry)
        diry = int(diry)
    direction = dirx, diry

    cur_coord = start
    while True:
        cur_coord = cur_coord[0] + direction[0], cur_coord[1] + direction[1]
        if cur_coord == end:
            break

        # flip any tiles along the way
        if new_board[cur_coord] == 1:
            new_board[cur_coord] = 2
            new_board.num_white_tiles -= 1
            new_board.num_black_tiles += 1

        elif new_board[cur_coord] == 2:
            new_board[cur_coord] = 1
            new_board.num_white_tiles += 1
            new_board.num_black_tiles -= 1

    lines = check_5_row(new_board)

    # while there are multiple to remove (unlikely) start removing them according to player input or bot choice
    player_lines = [l for l in lines if new_board[l[0]] == 1]
    bot_lines = [l for l in lines if new_board[l[0]] == 2]

    while len(bot_lines) > 1:
        line_num = pick_line_to_remove(new_board, lines)  # this could completely break lmao
        print(f"bot removed line: {convert_coord_to_output(lines[line_num][0])} - {convert_coord_to_output(lines[line_num][-1])}")
        remove_line(new_board, lines[line_num], True)

        lines = check_5_row(new_board)
        player_lines = [l for l in lines if new_board[l[0]] == 1]
        bot_lines = [l for l in lines if new_board[l[0]] == 2]

    while len(player_lines) > 1:
        prompt_remove_line(new_board, lines)

        lines = check_5_row(new_board)
        player_lines = [l for l in lines if new_board[l[0]] == 1]
        bot_lines = [l for l in lines if new_board[l[0]] == 2]

    if len(lines) == 1:
        remove_line(new_board, lines[0], new_board[lines[0][0]] == 2)
        print(f"removed line: {convert_coord_to_output(lines[0][0])} - {convert_coord_to_output(lines[0][-1])}")



    return new_board


def simulate_apply_move(board, move, color):
    new_board = board.deep_copy()
    if color == 1:
        simulate_apply_move_with_color(new_board, move, new_board.white_rings, color)
        new_board.num_white_tiles += 1
    else:
        simulate_apply_move_with_color(new_board, move, new_board.black_rings, color)
        new_board.num_black_tiles += 1

    return new_board


def simulate_apply_move_with_color(new_board, move, rings, color):
    start, end = move
    rings.remove(start)
    rings.add(end)
    new_board[start] = color
    new_board[end] = color + 2

    # create normalized direction
    dirx = end[0] - start[0]
    diry = end[1] - start[1]
    if abs(dirx) >= 1:
        dirx /= abs(dirx)
        dirx = int(dirx)
    if abs(diry) >= 1:
        diry /= abs(diry)
        diry = int(diry)
    direction = dirx, diry

    cur_coord = start
    while True:
        cur_coord = cur_coord[0] + direction[0], cur_coord[1] + direction[1]
        if cur_coord == end:
            break

        # flip any tiles along the way
        if new_board[cur_coord] == 1:
            new_board[cur_coord] = 2
            new_board.num_white_tiles -= 1
            new_board.num_black_tiles += 1

        elif new_board[cur_coord] == 2:
            new_board[cur_coord] = 1
            new_board.num_white_tiles += 1
            new_board.num_black_tiles -= 1

    lines = check_5_row(new_board)

    # while there are multiple to remove (unlikely) start removing them according to player input or bot choice
    while len(lines) > 0:
        line_num = 0
        remove_line(new_board, lines[line_num], True, simulation=True)
        lines = check_5_row(new_board)

    return new_board