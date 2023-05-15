import tkinter as tk
import ttkbootstrap as ttk
import solving


class Application(ttk.Frame):
    def __init__(self, master, sudoku, notes, ppppp,**kwargs):
        super().__init__(master, padding=5, **kwargs)
        self.create_style()
        self.grid(row=0, column=ppppp)
        # 数独区域
        self.playing = ttk.LabelFrame(self, labelanchor="nw", padding="10 10 10 10", text="数独")
        self.playing.grid(row=0, column=0, sticky=(ttk.N, ttk.W, ttk.E, ttk.S))
        self.plaid = [[None for i in range(9)] for i in range(9)]
        for i in range(3):
            for j in range(3):
                box = ttk.Frame(self.playing, style="TFrame", padding="3 3 3 3")
                box.grid(row=i, column=j)
                for m in range(3):
                    for n in range(3):
                        rr = i * 3 + m
                        cc = j * 3 + n
                        self.plaid[rr][cc] = ttk.Frame(box, style="TFrame", padding="1 1 1 1", height=81 + 2,
                                                       width=81 + 2)
                        self.plaid[rr][cc].grid(row=m, column=n)
                        self.plaid[rr][cc].grid_propagate(0)
                        self.create_cell(master=self.plaid[rr][cc], x=rr, y=cc, sudoku=sudoku, notes=notes)

    def create_style(self):
        ttk.Style().configure("TButton", font="TkFixedFont 41",)
        ttk.Style().configure("TEntry", font="TkFixedFont 41")
        ttk.Style().configure("TFrame",)
        ttk.Style().configure("TLabel")

    # def pa
    def create_cell(self, master, x, y, sudoku, notes):
        # cell = ttk.Button(self.plaid[rr][cc], text=str(sudoku[rr][cc]), style="TButton", width=2)
        # cell.grid(row=0, column=0)
        if sudoku[x][y] != 0:
            cell = ttk.Button(self.plaid[x][y], text=str(sudoku[x][y]), style="TButton", width=2)
            cell.grid(row=0, column=0)
        else:
            for i in range(3):
                for j in range(3):
                    if notes[i * 3 + j][x][y] == 0:
                        continue
                    l = ttk.Label(master, text=str(i * 3 + j+1), style="TLabel", borderwidth=0, font="TkFixedFont 16")
                    l.grid(row=i, column=j)
            # en = ttk.Entry(self.plaid[rr][cc],style="TEntry",exportselection=0,
            #                font="TkFixedFont 41",width=2)
            # en.grid(row=0,column=0,rowspan=3,columnspan=3)
