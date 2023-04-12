import numpy as np
import time
from frame import *
from solving import *

if __name__ == '__main__':
    len_all = 0
    len_a, len_b, len_c = 0, 0, 0
    # 解数独
    time_start = time.time()
    grid = Grid()
    # grid.sudoku_create_default()
    grid.sudoku_create_file("./原始数独.txt")
    grid.sudoku_init()
    while True:
        len_all += 1
        if grid.tactics_add():
            len_a += 1
            continue
        if grid.tactics_sub_notes_rc():
            len_b += 1
            continue
        if grid.tactics_sub_notes_box():
            len_c += 1
            continue
        break
    # grid.tactics_sub_notes_box()
    time_end = time.time()
    print("-------------------")
    print("<%s>难度，完成:%s，位置：%s，用时%.4f秒" % (grid.level, grid.completed, grid.sudoku_check(), time_end - time_start))
    print("策略一%d步 策略二%d步 策略三%d步" % (len_a, len_b, len_c))
    grid.sudoku_print()
    # exit()
    # 数独框架
    app = ttk.Window(
        title="数独工具 Power by Yallon",
        themename="cosmo",
        size=(1920, 960),
        # resizable=(False, False),
    )
    Application(app, sudoku=grid.sudoku_old, notes=grid.notes, ppppp=0)
    Application(app, sudoku=grid.sudoku, notes=grid.notes, ppppp=1)
    ttk.Label(app, text="共%d步，用时%s秒" % (len_all, time_end - time_start)).grid(row=1, column=0, columnspan=2)
    app.mainloop()
