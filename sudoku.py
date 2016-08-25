import random
import time

def create_grid():
    grid = []
    for row in range(9):
        grid.append([])
        for col in range(9):
            grid[row].append(0)
    return grid


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
    no_move = False
    row = 0

    values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(values)
    print("Seed: "),
    print(values)
    print("Test")

    temp_grid = create_grid()

    while row < 9:
        col = 0
        while col < 9:
            if no_move:
                grid[row][col] = 0
                temp_grid[row][col] = 0
                if col == 0 and row != 0:
                    row -= 1
                    col = 8
                elif col > 0:
                    col -= 1
                temp_grid[row][col] += 1
                no_move = False
                continue
            temp_index = temp_grid[row][col]
            if temp_index == 9:
                no_move = True
                continue
            grid[row][col] = values[temp_grid[row][col]]
            if not conflict(grid, row, col):
                col += 1
            else:
                temp_grid[row][col] += 1
        row += 1

    return grid


def print_grid(grid):
    for i in range(len(grid)):
        print(grid[i])

start = time.clock()
s_grid = create_grid()
s_grid = backtracking(s_grid)
end = time.clock()
print "Time: ",
print end - start
print_grid(s_grid)