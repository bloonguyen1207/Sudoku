import random
import time


def create_board():
    sudoku = [[0 for rows in range(9)] for cols in range(9)]
    trying = True
    while trying:
        sudoku = [[0 for rows in range(9)] for cols in range(9)]
        if generate_board(sudoku):
            trying = False
    return sudoku


def generate_board(board):

    vals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(vals)
    board[0] = vals[:]
    for row in range(9):
        for col in range(9):
            b = block(row / 3 + 1, col / 3 + 1, board)
            attempt = -1
            random.shuffle(vals)
            while board[row][col] == 0:
                dup = False
                attempt += 1

                if attempt >= 9:
                    return False

                value = vals[attempt]
                for i in range(col):
                    if value == board[row][i]:
                        dup = True
                        break

                for j in range(row):
                    if dup or value == board[j][col]:
                        dup = True
                        break
                if dup or value in b:
                    continue

                board[row][col] = value

    return True


def block(block_row, block_col, board):
    b = []
    row_idx = []
    col_idx = []
    if block_row == 1:
        row_idx = [0, 1, 2]
    elif block_row == 2:
        row_idx = [3, 4, 5]
    elif block_row == 3:
        row_idx = [6, 7, 8]

    if block_col == 1:
        col_idx = [0, 1, 2]
    elif block_col == 2:
        col_idx = [3, 4, 5]
    elif block_col == 3:
        col_idx = [6, 7, 8]

    for r in row_idx:
        for c in col_idx:
            b.append(board[r][c])
    return b


def print_board(board):

    if board is not None:
        print '     A   B   C     D   E   F     G   H   I'
        print '  +-------------+-------------+-------------+'
        for i in range(len(board)):
            print i + 1,
            print "|",
            for j in range(len(board[i])):
                print " " + str(board[i][j]) + " ",
                if (j + 1) % 3 == 0:
                    print "|",

            print '\n',
            if (i + 1) % 3 == 0:
                if i + 1 == 9:
                    print '  +-------------+-------------+-------------+'
                else:
                    print '  |-------------+-------------+-------------|'
    else:
        print "None"


def read_board(file_name):
    inp = open(file_name, 'r')
    data = inp.readline()
    raw_board = data.split(" ")
    completed_board = []
    for r in range(len(raw_board)):
        re = list(raw_board[r].strip('\n'))
        completed_board.append(re)
        for col in range(len(re)):
            re[col] = int(re[col])
    return completed_board


def get_missing(board):
    positions = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                missing = [i, j]
                positions.append(missing)
    return positions
# start = time.clock()
# game = create_board()
# end = time.clock()
# print "Time: ",
# print end - start
# print_board(game)
b = read_board("sudoku.txt")
print_board(b)
print get_missing(b)
