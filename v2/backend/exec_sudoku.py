import time
from solving import *


def exec_for():
    # 创建数独
    len_all = 0
    len_a, len_b, len_c = 0, 0, 0
    time_start = time.time()
    grid = Grid()
    grid.sudoku_create_file("./原始数独.txt")
    grid.sudoku_init()
    data_title = ''
    data_step = 0
    data_grids = grid.notes
    add_data(data_title, data_step, data_grids)

    # 解数独
    while True:
        len_all += 1
        if grid.tactics_add():
            data_title = '策略一'
            len_a += 1
            continue
        if grid.tactics_sub_notes_rc():
            data_title = '策略一'
            len_b += 1
            continue
        if grid.tactics_sub_notes_box():
            data_title = '策略一'
            len_c += 1
            continue
        data_step += 1
        data_grids = grid.way[-1]
        add_data(data_title, data_step, data_grids)
        break
    # grid.tactics_sub_notes_box()
    time_end = time.time()
    print("-------------------")
    print("<%s>难度，完成:%s，位置：%s，用时%.4f秒" % (
        grid.level, grid.completed, grid.sudoku_check(), time_end - time_start))
    print("策略一%d步 策略二%d步 策略三%d步" % (len_a, len_b, len_c))
    grid.sudoku_print()


def add_data(data_title, data_step, data_grids):
    title = data_title
    step = data_step
    grids = ''
    for i in range(9):
        for j in range(9):
            for k in range(9):
                grids += str(data_grids[i, j, k])
