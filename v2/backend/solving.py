import numpy as np


class Grid:
    @staticmethod
    def xy_to_mn(x, y):
        # m为宫格，n为宫格内第几个数
        # x为行，y为列
        m = x // 3 * 3 + y // 3
        n = x % 3 * 3 + y % 3
        return m, n

    @staticmethod
    def mn_to_xy(m, n):
        x = m // 3 * 3 + n // 3
        y = m % 3 * 3 + n % 3
        return x, y

    def __init__(self):
        self.completed = False
        self.level = "未知"
        self.count = 0
        self.sudoku_old = np.zeros((9, 9), dtype=np.int64)
        self.sudoku = np.zeros((9, 9), dtype=np.int64)
        self.notes = np.ones((9, 9, 9), dtype=np.int64)
        self.way = []
        # 状态判断
        self.notes_count_row = np.ones((9, 9)) * 9
        self.notes_count_col = np.ones((9, 9)) * 9
        self.notes_count_box = np.ones((9, 9)) * 9
        self.notes_count_cell = np.ones((9, 9)) * 9
        self.notes_vis_1 = np.zeros((9, 9), dtype=bool)
        self.notes_vis_2 = np.zeros((9, 9), dtype=bool)
        self.notes_vis_3 = np.zeros((9, 9), dtype=bool)

    def sudoku_create_default(self):
        self.sudoku_old = np.array(
            [[5, 9, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 7, 9, 4, 0, 0],
             [0, 4, 7, 1, 2, 5, 8, 0, 0],
             [2, 6, 0, 0, 0, 0, 7, 4, 0],
             [1, 3, 0, 0, 6, 0, 9, 0, 8],
             [0, 5, 0, 0, 0, 3, 2, 6, 1],
             [9, 7, 0, 0, 8, 6, 0, 0, 4],
             [4, 1, 0, 0, 5, 2, 6, 8, 0],
             [6, 8, 5, 9, 4, 0, 0, 0, 7], ]
        )

    def sudoku_create_file(self, file):
        f = open(file, "r", encoding="utf-8")
        self.level = f.readline()[:-1]
        for i in range(9):
            text = f.readline()
            for j, val in enumerate(text):
                if val == "\n":
                    continue
                elif val == " " or val == "0":
                    self.sudoku_old[i][j] = 0
                else:
                    self.sudoku_old[i][j] = int(val)
        f.close()

    def sudoku_init(self):
        # 初始化笔记和数独
        for x, text in enumerate(self.sudoku_old):
            for y, val in enumerate(text):
                if val != 0:
                    self.xy_add_val(x, y, val)

    def sudoku_check(self):
        for i in range(9):
            for j in range(9):
                correct, x, y = self.xy_check(i, j)
                if not correct:
                    return False, x, y
        return True

    def sudoku_print(self):
        print(
            # "数独完成：%s" % self.completed,
            # self.notes_count_row,
            # self.notes_count_col,
            # self.notes_count_box,
            # self.notes_count_cell,
            sep="\n")
        pass

    def tactics_add(self):
        # 位置数判断
        row, col = np.where(self.notes_count_cell == 1)
        for k, _ in enumerate(row):
            pos = np.where(self.notes[:, row[k], col[k]])
            self.xy_add_val(row[k], col[k], pos[0][0] + 1)
            return True
        # 行数判断
        row, pos = np.where(self.notes_count_row == 1)
        for k, _ in enumerate(pos):
            col = np.where(self.notes[pos[k], row[k], :])
            self.xy_add_val(row[k], col[0], pos[k] + 1)
            return True
        # 列数判断
        col, pos = np.where(self.notes_count_col == 1)
        for k, _ in enumerate(pos):
            row = np.where(self.notes[pos[k], :, col[k]])
            self.xy_add_val(row[0], col[k], pos[k] + 1)
            return True
        # 宫数判断
        box, pos = np.where(self.notes_count_box == 1)
        for k, _ in enumerate(pos):
            start_x = box[k] // 3 * 3
            start_y = box[k] % 3 * 3
            box_re = np.where(self.notes[pos[k], start_x:start_x + 3, start_y:start_y + 3])
            self.xy_add_val(start_x + box_re[0][0], start_y + box_re[1][0], pos[k] + 1)
            return True
        return False

    def tactics_sub_notes_rc(self):
        #  宫区块数对和宫区块三数组，旨在消除所属row and column的该笔记
        box, pos = np.where((self.notes_count_box == 2) | (self.notes_count_box == 3))
        for k, _ in enumerate(pos):
            if self.notes_vis_1[box[k], pos[k]]:
                continue
            self.notes_vis_1[box[k], pos[k]] = True
            start_x, start_y = self.mn_to_xy(box[k], 0)
            box_re = np.where(self.notes[pos[k], start_x:start_x + 3, start_y:start_y + 3])
            # 消行
            if len(box_re[0]) == 2 and box_re[0][0] == box_re[0][1] or \
                    len(box_re[0]) == 3 and box_re[0][0] == box_re[0][1] and box_re[0][1] == box_re[0][2]:
                for j in range(9):
                    if j == start_y or j == start_y + 1 or j == start_y + 2:
                        continue
                    self.xy_sub_notes(start_x + box_re[0][0], j, pos[k])
                return True
            #  消列
            if len(box_re[0]) == 2 and box_re[1][0] == box_re[1][1] or \
                    len(box_re[0]) == 3 and box_re[1][0] == box_re[1][1] and box_re[1][1] == box_re[1][2]:
                for i in range(9):
                    if i == start_x or i == start_x + 1 or i == start_x + 2:
                        continue
                    self.xy_sub_notes(i, start_y + box_re[1][0], pos[k])
                return True
        return False

    def tactics_sub_notes_box(self):
        # 显性数对和显性三数组，旨在消除所在box的该笔记
        for k in range(9):
            start_x, start_y = self.mn_to_xy(k, 0)
            box = self.notes_count_cell[start_x:start_x + 3, start_y:start_y + 3]
            print(k,box)
            u, v = np.where(box == 2)
            if u.size <= 1 or u.size >= 3:
                continue
            # 显性数对
            for p_in in range(u.size):
                x1, y1 = start_x + u[p_in], start_y + v[p_in]
                if (x1, y1) in self.notes_vis_2 and self.notes_vis_2[(x1, y1)]:
                    continue
                self.notes_vis_2[(x1, y1)] = True
                for q_in in range(p_in + 1, u.size):
                    x2, y2 = start_x + u[q_in], start_y + v[q_in]
                    if (self.notes[:, x1, y1] == self.notes[:, x2, y2]).all():
                        note_tmp = np.where(self.notes[:, x1, y1])
                        note1, note2 = note_tmp[0][0], note_tmp[0][1]
                        # 消除所在box的该笔记
                        for i in range(3):
                            for j in range(3):
                                if i == u[p_in] and j == v[p_in] or i == u[q_in] and j == v[q_in]:
                                    continue
                                self.xy_sub_notes(start_x + i, start_y + j, note1)
                                self.xy_sub_notes(start_x + i, start_y + j, note2)
                        return True
        return False

    def tactics_sub_notes_cell(self):
        # 隐形数对和隐形三数组，旨在消除所在cell的其它笔记
        # for box in range(9):
        #     start_x,start_y = self.mn_to_xy(box,0)
        #     pos = np.where(self.notes_count_box[box,:]==2)
        #     # if pos.size == 1 or pos.size
        pass

    """ 
    以下为共性操作
    """

    def xy_add_val(self, x, y, val):
        self.sudoku[x, y] = val
        start_x = x // 3 * 3
        start_y = y // 3 * 3
        # 自己的笔记全部消除
        for k in range(9):
            self.xy_sub_notes(x, y, k)
        # 更新邻居笔记
        for k in range(9):
            self.xy_sub_notes(x, k, val - 1)
            self.xy_sub_notes(k, y, val - 1)
            self.xy_sub_notes(start_x + k // 3, start_y + k % 3, val - 1)
        self.count += 1
        if self.count == 81:
            self.completed = True
        self.way.append(self.notes.copy())

    def xy_sub_notes(self, x, y, pos):
        if self.notes[pos, x, y] == 0:
            return
        self.notes[pos, x, y] = 0
        self.notes_count_row[x, pos] -= 1
        self.notes_count_col[y, pos] -= 1
        self.notes_count_box[x // 3 * 3 + y // 3, pos] -= 1
        self.notes_count_cell[x, y] -= 1
        self.way.append(self.notes.copy())

    def xy_check(self, x, y):
        # 行检查
        num_count = [0 for k in range(9)]
        for j in range(9):
            if self.sudoku[x, j] == 0:
                continue
            num_count[self.sudoku[x, j] - 1] += 1
            if num_count[self.sudoku[x, j] - 1] >= 2:
                return False, x, j

        # 列检查
        num_count = [0 for k in range(9)]
        for i in range(9):
            if self.sudoku[i, y] == 0:
                continue
            num_count[self.sudoku[i, y] - 1] += 1
            if num_count[self.sudoku[i, y] - 1] >= 2:
                return False, i, y
        # 宫检查
        m, _ = self.xy_to_mn(x, y)
        num_count = [0 for k in range(9)]
        for n in range(9):
            if self.sudoku[self.mn_to_xy(m, n)] == 0:
                continue
            num_count[self.sudoku[self.mn_to_xy(m, n)] - 1] += 1
            if num_count[self.sudoku[self.mn_to_xy(m, n)] - 1] >= 2:
                return False, self.mn_to_xy(m, n)
        return True, -1, -1

# if __name__ == '__main__':
#     self = Grid()
#     self.sudoku_create()
#     self.sudoku_init()
