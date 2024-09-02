max_dimension = 11

def create_grid_from_file(board):
    def validate(coord, valid_coords):
        if coord in valid_coords:
            return 0
        return -1

    valid_coords = set()
    with open("valid_coords.txt") as file:
        for line in file:
            line = line.strip()
            letter, line = line[0], line[1:]
            letter = letter_to_int(letter)
            line = line.split('-')
            start = int(line[0]) - 1
            end = int(line[1]) - 1
            for i in range(start, end+1):
                valid_coords.add((letter, i))
    board.valid_coords = valid_coords

    board.grid = [[validate((row, col), valid_coords) for col in range(max_dimension)] for row in range(max_dimension)]


def letter_to_int(letter):
    return ord(letter) - 97


def int_to_letter(num):
    return chr(num+97)


def convert_input_to_coord(input_str):
    letter = input_str[0]
    num = int(input_str[1:])
    num -= 1
    return letter_to_int(letter), num


def convert_coord_to_output(coord):
    return f"{int_to_letter(coord[0])}{coord[1]+1}"


def flip_player(player):
    if player == 1:
        return 2
    return 1