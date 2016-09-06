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

                for k in range(len(b)):
                    if dup or value in b[k]:
                        break

                if dup:
                    continue
                board[row][col] = value

    return True


def block(x, y, board):
    b = []
    br = []
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
            br.append(board[r][c])
        b.append(br)
        br = []
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
    for i in range(len(board)):
        if row[i] > 0:
            not_answer.append(row[i])
        if col[i] > 0:
            not_answer.append(col[i])
        for j in range(3):
            if p_block[i/3][j] > 0:
                not_answer.append(p_block[i/3][j])

    for i in range(1, 10):
        if i not in not_answer:
            possible_answers.append(i)

    return possible_answers


def solve(board):
    missing_spots = get_missing(board)
    old_len = len(missing_spots)
    rcb_not_working = False
    not_working = False
    while missing_spots:
        for i in range(len(missing_spots)):
            pos_ans = get_possible_answers(missing_spots[i], board)
            if len(pos_ans) == 1:
                board[missing_spots[i][0]][missing_spots[i][1]] = pos_ans[0]
            if i == len(missing_spots) - 1:
                missing_spots = get_missing(board)
                if len(missing_spots) == old_len:
                    rcb_not_working = True
                    break
                else:
                    old_len = len(missing_spots)

        if rcb_not_working:
            for i in range(len(missing_spots)):
                for j in range(3):
                    lone_rangers(j, missing_spots[i], missing_spots)
            missing_spots = get_missing(board)
            if len(missing_spots) == old_len:
                not_working = True
            else:
                old_len = len(missing_spots)

            if not_working:
                return False

    return True

# start = time.clock()
# game = create_board()
# end = time.clock()
# print "Time: ",
# print end - start
# print_board(game)


def same_row(element, arr):
    sr = []
    row = element[0]
    for i in range(len(arr)):
        if arr[i][0] == row:
            sr.append(arr[i])

    return sr


def same_col(element, arr):
    sc = []
    col = element[1]
    for i in range(len(arr)):
        if arr[i][1] == col:
            sc.append(arr[i])

    return sc


def same_block(element, arr):
    sb = []
    br = element[0] / 3
    bc = element[1] / 3
    for i in range(len(arr)):
        if arr[i][0] / 3 == br and arr[i][1] / 3 == bc:
            sb.append(arr[i])

    return sb


def lone_rangers(t, position, arr):
    cell_info = []
    missing_elements = []
    possible_answers = []
    test = []
    if t is 0:
        test = same_block(position, arr)
    elif t is 1:
        test = same_row(position, arr)
    elif t is 2:
        test = same_col(position, arr)
    for i in range(len(test)):
        possible_answer = get_possible_answers(test[i], b)
        possible_answers.append(possible_answer)

    for i in range(len(possible_answers)):
        for j in range(len(possible_answers[i])):
            cell_info.append([possible_answers[i][j], test[i], 0])
            missing_elements.append(possible_answers[i][j])

    s1 = list(set(missing_elements))

    for i in range(len(s1)):
        for j in range(len(cell_info)):
            if cell_info[j][0] == s1[i]:
                cell_info[j][2] = missing_elements.count(s1[i])

    for i in range(len(cell_info)):
        if cell_info[i][2] == 1:
            b[cell_info[i][1][0]][cell_info[i][1][1]] = cell_info[i][0]


b = read_board("sudoku.txt")
print_board(b)
print solve(b)
#     print "It didn't work"
# else:
#     print "Solved"

print_board(b)

missing = get_missing(b)
print missing

