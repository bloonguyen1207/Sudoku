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


def block(x, y, board):
    b = []
    row_idx = []
    col_idx = []
    if x == 1:
        row_idx = [0, 1, 2]
    elif x == 2:
        row_idx = [3, 4, 5]
    elif x == 3:
        row_idx = [6, 7, 8]

    if y == 1:
        col_idx = [0, 1, 2]
    elif y == 2:
        col_idx = [3, 4, 5]
    elif y == 3:
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


def get_column(position, board):
    col = []
    for j in range(len(board)):
        col.append(board[j][position[1]])

    return col


def get_row(position, board):
    row = []
    for i in range(len(board)):
        row.append(board[position[0]][i])

    return row


def get_possible_answers(position, board):
    row = get_row(position, board)
    col = get_column(position, board)
    p_block = block(position[0] / 3 + 1, position[1] / 3 + 1, board)
    not_answer = []
    possible_answers = []
    for i in range(9):
        if row[i] > 0:
            not_answer.append(row[i])
        if col[i] > 0:
            not_answer.append(col[i])
        if p_block[i] > 0:
            not_answer.append(p_block[i])

    for i in range(1, 10):
        if i not in not_answer:
            possible_answers.append(i)

    return possible_answers

# start = time.clock()
# game = create_board()
# end = time.clock()
# print "Time: ",
# print end - start
# print_board(game)
b = read_board("sudoku.txt")
print_board(b)
missing_elements = get_missing(b)
print missing_elements

print get_row(missing_elements[0], b)

while missing_elements:
    for i in range(len(missing_elements)):
        pos_ans = get_possible_answers(missing_elements[i], b)
        print pos_ans

        if len(pos_ans) == 1:
            b[missing_elements[i][0]][missing_elements[i][1]] = pos_ans[0]
        if i == len(missing_elements) - 1:
            missing_elements = get_missing(b)
    print missing_elements
    print_board(b)

print_board(b)
