import random
import time


# ------------------Bloo generates full board (brute force) from here-----------------------
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
                        dup = True
                        break

                if dup:
                    continue
                board[row][col] = value

    return True


# ------------------Mai generates full board (back tracking) from here-----------------------
def create_grid():
    grid = []
    for row in range(9):
        grid.append([])
        for col in range(9):
            grid[row].append(0)
    return grid


# check if there is that value in row, col, block from the beginning to that position
def conflict(grid, row, col):
    for i in range(0, col):
        if grid[row][col] == grid[row][i]:
            return True

    for i in range(0, row):
        if grid[row][col] == grid[i][col]:
            return True

    row_block = row // 3 * 3
    col_block = col // 3 * 3
    for i in range(row_block, row_block + 3):
        for j in range(col_block, col_block + 3):
            if i == row and j == col:
                return False
            if grid[row][col] == grid[i][j]:
                return True

    return False


def backtracking(grid):
    temp_grid = []
    for row in range(9):
        temp_grid.append([])
        for col in range(9):
            temp_grid[row].append([])

    no_move = False
    row = 0

    while row < 9:
        col = 0
        while col < 9:
            if no_move:
                grid[row][col] = 0
                temp_grid[row][col] = []
                if col == 0 and row != 0:
                    row -= 1
                    col = 8
                elif col > 0:
                    col -= 1
                no_move = False
                continue
            temp_value = random.randrange(1, 10)
            while temp_value in temp_grid[row][col] and len(temp_grid[row][col]) < 9:
                temp_value = random.randrange(1, 10)
            if len(temp_grid[row][col]) == 9:
                no_move = True
                continue
            temp_grid[row][col].append(temp_value)
            grid[row][col] = temp_value
            if not conflict(grid, row, col):
                col += 1
        row += 1

    return grid


# ------------------Mai first / second attemp to dig number------------------------------------
# check neu o do chi chua duoc 1 value (8 values con` lai deu xuat hien), xoa
def fst_easy_check(grid, row, col):
    check = 0
    temp_value = grid[row][col]
    for i in range(1, 10):
        grid[row][col] = i
        if appearance(grid, row, col):
            check += 1
    # print("check " + str(check))
    grid[row][col] = temp_value
    if check >= 8:
        return True
    else:
        return False


# check neu cac empty cell trong row, col, block tuong ung' deu khong chua dc value, xoa
def sec_easy_check(grid, row, col):
    check = 0
    count_empty = 0
    original = grid[row][col]
    grid[row][col] = 0
    # check empty cells in row
    for i in range(0, 9):
        if i == col:
            continue
        if grid[row][i] == 0:
            count_empty += 1
            temp_value = grid[row][i]
            grid[row][i] = original
            if appearance(grid, row, i):
                grid[row][i] = temp_value
                check += 1
            else:
                grid[row][i] = temp_value
                break
    if count_empty == check:
        grid[row][col] = original
        return True
    else:
        check = 0
        count_empty = 0

    # check empty cells in col
    for i in range(0, 9):
        if i == row:
            continue
        if grid[i][col] == 0:
            count_empty += 1
            temp_value = grid[i][col]
            grid[i][col] = original
            if appearance(grid, i, col):
                grid[i][col] = temp_value
                check += 1
            else:
                grid[i][col] = temp_value
                break
    if count_empty == check:
        grid[row][col] = original
        return True
    else:
        check = 0
        count_empty = 0

    # check empty cells in block
    row_block = row // 3 * 3
    col_block = col // 3 * 3
    for i in range(row_block, row_block + 3):
        for j in range(col_block, col_block + 3):
            if i == row and j == col:
                continue
            if grid[i][j] == 0:
                count_empty += 1
                temp_value = grid[i][j]
                grid[i][j] = original
                if appearance(grid, i, j):
                    grid[i][j] = temp_value
                    check += 1
                else:
                    grid[i][j] = temp_value
                    break
    grid[row][col] = original
    if count_empty == check:
        return True
    else:
        return False


def delete_cell(grid):
    temp_grid = []
    erase_num = 0
    finish = False
    while not finish:
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] != 0:
                    if fst_easy_check(grid, row, col):
                        temp_grid.append([row, col])
        if not temp_grid:
            break

        # print(temp_grid)
        rand_index = random.randrange(0, len(temp_grid))
        grid[temp_grid[rand_index][0]][temp_grid[rand_index][1]] = 0
        erase_num += 1
        temp_grid = []
        # print("-------------------------")
        # print_grid(grid)

    print("1st Erase number: " + str(erase_num))

    finish = False
    while not finish:
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] != 0:
                    if sec_easy_check(grid, row, col):
                        temp_grid.append([row, col])
        if not temp_grid:
            break

        # print(temp_grid)
        rand_index = random.randrange(0, len(temp_grid))
        grid[temp_grid[rand_index][0]][temp_grid[rand_index][1]] = 0
        erase_num += 1
        temp_grid = []
        # print("-------------------------")
        # print_grid(grid)

    print("2st Erase number: " + str(erase_num))
    print("Remain: " + str(81 - erase_num))
    return grid


# ------------------Mai final algo to dig number----------------------------------------------
# check if there is that value in row, col, block
def appearance(grid, row, col):
    # print("row col: " + str(row) + " " + str(col))
    # print("appearance " + str(grid[row][col]))
    for i in range(0, 9):
        if i == col:
            continue
        # print(i)
        # print("row " + str(grid[row][i]))
        # print(grid[row][col]),
        # print(grid[row][i])
        if grid[row][col] == grid[row][i]:
            # print("row " + "True")
            return True
    for i in range(0, 9):
        # print("col " + str(grid[i][col]))
        if i == row:
            continue
        if grid[row][col] == grid[i][col]:
            # print("col " + "True")
            return True

    row_block = row // 3 * 3
    col_block = col // 3 * 3
    for i in range(row_block, row_block + 3):
        for j in range(col_block, col_block + 3):
            if i == row and j == col:
                continue
            if grid[row][col] == grid[i][j]:
                # print("block " + str(grid[i][j]))
                return True
    # print(False)
    return False


def create_guess_list(grid):
    guess_grid = []
    for row in range(9):
        guess_grid.append([])
        for col in range(9):
            guess_grid[row].append([])

    for i in range(0, 9):
        for j in range(0, 9):
            if grid[i][j] == 0:
                # print("-----" + str(i) + "----" + str(j) + "-----")
                for k in range(1, 10):
                    grid[i][j] = k
                    do_append = not appearance(grid, i, j)
                    # print(str(k) + " " + str(do_append))
                    if do_append:
                        # print("append")
                        guess_grid[i][j].append(k)
                grid[i][j] = 0

    return guess_grid


def check_guess_pos(guess_grid, row, col):
    if len(guess_grid[row][col]) == 1:
        return True
    return False


def remove_guess_num(guess_grid, row, col, value):
    for i in range(0, 9):
        if i == col:
            continue
        if value in guess_grid[row][i]:
            # print(value in guess_grid[row][i])
            # print value
            # print guess_grid[row][i]
            guess_grid[row][i].remove(value)

    for i in range(0, 9):
        # print("col " + str(grid[i][col]))
        if i == row:
            continue
        if value in guess_grid[i][col]:
            # print("col " + "True")
            # print(value in guess_grid[i][col])
            # print value
            # print guess_grid[i][col]
            guess_grid[i][col].remove(value)

    row_block = row // 3 * 3
    col_block = col // 3 * 3
    for i in range(row_block, row_block + 3):
        for j in range(col_block, col_block + 3):
            if i == row and j == col:
                continue
            if value in guess_grid[i][j]:
                # print("block " + str(grid[i][j]))
                guess_grid[i][j].remove(value)

    return guess_grid


def update_guess_list(guess_grid):
    check = 0
    while True:
        no_move = check
        check = 0
        for i in range(0, 9):
            for j in range(0, 9):
                if check_guess_pos(guess_grid, i, j):
                    temp_value = guess_grid[i][j][0]
                    remove_guess_num(guess_grid, i, j, temp_value)
                    check += 1
        if no_move == check:
            break
    return guess_grid


def erase_number(grid, remain_num):
    temp_grid = []
    erase_num = 0
    finish = False

    # randomly delete 20 num
    while erase_num < 20:
        row = random.randrange(0, 9)
        col = random.randrange(0, 9)
        if grid[row][col] != 0:
            erase_num += 1
            grid[row][col] = 0

    # continue deleting but at each iteration, check if the cell is possible to delete
    while not finish and erase_num < 81 - remain_num:
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] != 0:
                    temp_value = grid[row][col]
                    grid[row][col] = 0
                    guess_grid = create_guess_list(grid)
                    guess_grid = update_guess_list(guess_grid)
                    if check_guess_pos(guess_grid, row, col):
                        temp_grid.append([row, col])
                    grid[row][col] = temp_value
        if not temp_grid:
            break

        # print(temp_grid)
        rand_index = random.randrange(0, len(temp_grid))
        grid[temp_grid[rand_index][0]][temp_grid[rand_index][1]] = 0
        erase_num += 1
        temp_grid = []
        # print("-------------------------")
        # print_grid(grid)

    print("Erase number: " + str(erase_num))
    print("Remain: " + str(81 - erase_num))
    return grid


# ------------------Mai store grid into file--------------------------------------------------
def store_grid(grid, file_name):
    # output_file = open("unsolved_sudoku.txt", 'w')
    output_file = open(file_name, 'w')
    for row_num in range(len(grid)):
        for num in grid[row_num]:
            output_file.write(str(num))
        if row_num != len(grid) - 1:
            output_file.write(" ")
    output_file.close()


# ------------------Bloo solve sudoku---------------------------------------------------------
# Function to return elements in a specific block, first block x, y is 1, 1
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


# Function to print sudoku board in a nice format
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


# Function to read a sudoku board from a txt file
# Sample: 302609005 500730000 000000900 000940000 000000109 000057060 008500006 000000003 019082040
def read_board(inp):
    # inp = open(file_name, 'r')
    data = inp.readline()
    raw_board = data.split(" ")
    completed_board = []
    for r in range(len(raw_board)):
        re = list(raw_board[r].strip('\n'))
        completed_board.append(re)
        for col in range(len(re)):
            re[col] = int(re[col])
    # inp.close()
    return completed_board


# Function that return the positions of the missing spots in the board
def get_missing(board):
    positions = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                missing = [i, j]
                positions.append(missing)
    return positions


# Function to get all elements in the same column of a specific position
def get_column(position, board):
    col = []
    for j in range(len(board)):
        col.append(board[j][position[1]])

    return col


# Function to get all elements in the same row of a specific position
def get_row(position, board):
    row = []
    for i in range(len(board)):
        row.append(board[position[0]][i])

    return row


# Function to get all elements in the same block of a specific position
def get_block(element, arr):
    sb = []
    br = element[0] / 3
    bc = element[1] / 3
    for i in range(len(arr)):
        if arr[i][0] / 3 == br and arr[i][1] / 3 == bc:
            sb.append(arr[i])

    return sb


# Function to get possible answer by checking row, block, column of a specific position
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


# Check the length of the possible answer array, if there's only 1 element in the array, it's the answer
# If the 1st solution doesn't work, try apply lone ranger technique
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
                if i == len(missing_spots) - 1:
                    missing_spots = get_missing(board)
                    if len(missing_spots) == old_len:
                        not_working = True
                        break
                    else:
                        old_len = len(missing_spots)

            if not_working:
                print_board(board)
                return False

    print_board(board)
    return True

# Same as get_row and get_column

# def same_row(element, arr):
#     sr = []
#     row = element[0]
#     for i in range(len(arr)):
#         if arr[i][0] == row:
#             sr.append(arr[i])
#
#     return sr
#
#
# def same_col(element, arr):
#     sc = []
#     col = element[1]
#     for i in range(len(arr)):
#         if arr[i][1] == col:
#             sc.append(arr[i])
#
#     return sc


# Check the number of occurrence of an answer in either a block, row or column, if it only appear once, it's the answer
def lone_rangers(t, position, arr):
    cell_info = []
    missing_elements = []
    possible_answers = []
    test = []
    if t is 0:
        test = get_block(position, arr)
    elif t is 1:
        test = get_row(position, arr)
    elif t is 2:
        test = get_column(position, arr)
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


# -------------------Main---------------------------------------------------
num_remain = 26
num_grid = 1
inp_file = "unsolved_sudoku.txt"


# ---Bloo generates full board---
s_grid = create_board()

# ---Mai generates full board---
# s_grid = create_grid()
# s_grid = backtracking(s_grid)


print_board(s_grid)

s_grid = erase_number(s_grid, num_remain)
print_board(s_grid)
store_grid(s_grid, "unsolved_sudoku.txt")


inpt = open(inp_file, 'r')
success = 0
start = time.clock()

for i in range(num_grid):
    b = read_board(inpt)
    if solve(b):
        success += 1

end = time.clock()
print "Time: ",
print end - start
print "Solved " + str(success) + "/" + str(num_grid)

