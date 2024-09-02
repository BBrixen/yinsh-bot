from gameplay_mechanics import valid_moves, simulate_apply_move
from utils import flip_player
default_max_depth = 5
bot_version = 'pablo'

def evaluate_board(board):
    if bot_version == 'carlos':
        return evaluate_board_carlos(board)
    elif bot_version == 'michael':
        return evaluate_board_michael(board)
    elif bot_version == 'pablo':
        return evaluate_board_pablo(board)


def convert_num_valid_moves_to_max_depth(num_valid_moves, starting_valid_moves):
    if bot_version == 'carlos':
        return default_max_depth
    if num_valid_moves <= 0.2 * starting_valid_moves:
        return default_max_depth + 2
    if num_valid_moves <= 0.5 * starting_valid_moves:
        return default_max_depth + 1
    return default_max_depth


def evaluate_board_michael(board):
    # larger number means black is doing better
    # bot wants to maximize, player is minimizing
    if board.winner != 0:
        # sensitized to win by larger margin and lose by lesser margin
        return 1000 * (board.black_points - board.white_points)

    # no winner
    return 100 * (board.black_points - board.white_points) + (board.num_black_tiles - board.num_white_tiles)

def evaluate_board_pablo(board):
    if board.winner != 0:
        # sensitized to win by larger margin and lose by lesser margin
        return 1000 * (board.black_points - board.white_points)

    # no winner
    return (100 * (board.black_points - board.white_points) + 20 * (board.num_black_4_rows - board.num_white_4_rows) +
            10 * (board.num_black_3_rows - board.num_white_3_rows) + (board.num_black_tiles - board.num_white_tiles))


def evaluate_board_carlos(board):
    """return numeric value to represent how favorable this board is"""
    # largest number means that black is doing better
    # bot is maximizing, player is minimizing

    if board.winner == 2:
        return 1_000_000
    if board.winner != 0:
        return -1_000_000

    return 100 * (board.black_points - board.white_points) + (board.num_black_tiles - board.num_white_tiles)

def print_board_eval(board, best_score, depth):
    print(f"in favor of black:")
    print(f"point difference {board.black_points - board.white_points}")
    print(f"4 row difference {board.num_black_4_rows - board.num_white_4_rows}")
    print(f"3 row difference {board.num_black_3_rows - board.num_white_3_rows}")
    print(f"tile difference  {board.num_black_tiles - board.num_white_tiles}")
    print(f"evaluation of current board: {evaluate_board(board)}")
    print(f"bot evaluation of board in {depth} moves: {best_score}\n")


def get_bot_move(board, cur_player, starting_valid_moves):
    num_valid_moves = len(valid_moves(board, cur_player))
    print(f"{num_valid_moves=}")
    bot_depth = convert_num_valid_moves_to_max_depth(num_valid_moves, starting_valid_moves)
    best_score, move = get_series_of_moves_with_best_board(board, cur_player,True, float('-inf'),
                                                           float('inf'), bot_depth)
    print_board_eval(board, best_score, bot_depth)
    return move


def get_series_of_moves_with_best_board(board, cur_player, maximizing, alpha, beta, depth):
    if depth <= 1 or board.winner != 0:
        return evaluate_board(board), None

    moves = valid_moves(board, cur_player)
    best_move = None

    if maximizing:
        best_score = float('-inf')
        for move in moves:
            new_board = simulate_apply_move(board, move, cur_player)
            best_score_from_move, future_move \
                = get_series_of_moves_with_best_board(new_board, flip_player(cur_player), not maximizing, alpha, beta,
                                                      depth=depth - 1)
            if best_score_from_move > best_score:
                best_score = best_score_from_move
                best_move = move

            alpha = max(alpha, best_score_from_move)
            if beta <= alpha:
                break
    else:
        best_score = float('inf')
        for move in moves:
            new_board = simulate_apply_move(board, move, cur_player)
            best_score_from_move, future_move \
                = get_series_of_moves_with_best_board(new_board, flip_player(cur_player), not maximizing, alpha, beta, depth=depth - 1)

            if best_score_from_move < best_score:
                best_score = best_score_from_move
                best_move = move

            beta = min(beta, best_score_from_move)
            if beta <= alpha:
                break

    return best_score, best_move


def pick_ring_to_remove(board, rings_list):
    from gameplay_mechanics import remove_ring

    max_i = 0
    best_score = None
    depth = default_max_depth

    for i, ring in enumerate(rings_list):
        new_board = board.deep_copy()
        remove_ring(new_board, board[ring]-2, ring)

        score, move = get_series_of_moves_with_best_board(new_board, 1, False, float('-inf'),
                                                          float('inf'), depth)
        if best_score is None or score > best_score:
            best_score = score
            max_i = i
    return max_i



def pick_line_to_remove(board, lines):
    # current plan: evaluate board after 4 moves for all lines removed, and pick the one with the best state
    # this could turn out to be very slow,
    from gameplay_mechanics import remove_line
    if len(lines) == 0:
        return 0

    max_i = 0
    best_score = None
    depth = default_max_depth

    for i, line in enumerate(lines):
        new_board = board.deep_copy()
        remove_line(new_board, line, True)

        score, move = get_series_of_moves_with_best_board(new_board, 1, False, float('-inf'),
                                                          float('inf'), depth)
        if best_score is None or score > best_score:
            max_i = i
            best_score = score
    return max_i