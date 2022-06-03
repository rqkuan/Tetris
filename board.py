from tkinter import *
from pieces import *


class Board:

    def __init__(self, root):
        self.board = [[Block(i, j) for i in range(10)] for j in range(21)]
        for i in self.board:
            for b in i:
                b.canvas = Canvas(root, width=24, height=24, bg="black", highlightthickness=1, highlightbackground="black")
                b.canvas.grid(column=b.x + 8, row=b.y)
        for b in self.board[20]:
            b.canvas.config(bg="gray", highlightbackground="gray")

    def line_is_full(self, line):
        full = True
        for i in range(10):
            if self.board[line][i].canvas["background"] == "black":
                full = False
        return full

    def clear_line(self, line):
        for i in range(line):
            for j in range(10):
                self.board[line-i][j].canvas.config(bg=self.board[line-i-1][j].canvas["background"])
        for i in range(10):
            self.board[0][i].canvas.config(bg="black")

    def below_is_empty(self, blocks):
        empty = True
        checklist = []
        lowest = []
        for b in blocks:
            if b.x not in checklist:
                checklist.append(b.x)
                lowest.append(0)
        for i in range(len(checklist)):
            for b in blocks:
                if b.x == checklist[i] and b.y > lowest[i]:
                    lowest[i] = b.y
        for i in range(len(checklist)):
            if self.board[lowest[i] + 1][checklist[i]].canvas["background"] not in ["black", "gray"] or \
                    self.board[lowest[i] + 1][checklist[i]].canvas["highlightbackground"] != "black":
                empty = False
        return empty

    @staticmethod
    def out_of_bounds(x):
        if x > 9 or x < 0:
            return True
        return False

    def left_is_empty(self, blocks):
        empty = True
        checklist = []
        left_most = []
        for b in blocks:
            if b.y not in checklist:
                checklist.append(b.y)
                left_most.append(11)
        for i in range(len(checklist)):
            for b in blocks:
                if b.y == checklist[i] and b.x < left_most[i]:
                    left_most[i] = b.x
        for i in range(len(checklist)):
            if self.out_of_bounds(left_most[i] - 1):
                empty = False
            elif self.board[checklist[i]][left_most[i] - 1].canvas["background"] not in ["black", "gray"] or \
                    self.board[checklist[i]][left_most[i] - 1].canvas["highlightbackground"] != "black":
                empty = False
        return empty

    def right_is_empty(self, blocks):
        empty = True
        checklist = []
        right_most = []
        for b in blocks:
            if b.y not in checklist:
                checklist.append(b.y)
                right_most.append(0)
        for i in range(len(checklist)):
            for b in blocks:
                if b.y == checklist[i] and b.x > right_most[i]:
                    right_most[i] = b.x
        for i in range(len(checklist)):
            if self.out_of_bounds(right_most[i] + 1):
                empty = False
            elif self.board[checklist[i]][right_most[i] + 1].canvas["background"] not in ["black", "gray"] or \
                    self.board[checklist[i]][right_most[i] + 1].canvas["highlightbackground"] != "black":
                empty = False
        return empty

    def check_rotate(self, piece, blocks, offsetX=0, offsetY=0):
        empty = True
        piece.draw(blocks, "black")
        for b in blocks:
            checkY = piece.refY + b.x - piece.refX + offsetY
            checkX = piece.refX + 3 - b.y + piece.refY + offsetX
            if self.out_of_bounds(checkX):
                empty = False
            elif self.board[checkY][checkX].canvas["background"] not in ["black", "gray"] or \
                    self.board[checkY][checkX].canvas["highlightbackground"] != "black":
                empty = False
        if not empty:
            piece.draw(blocks, piece.color)
        return empty
