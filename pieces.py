class Block:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Piece:

    def __init__(self, root, board):
        self.board = board
        self.root = root
        self.pause = False
        self.fallen = False
        self.death = False
        self.root.bind('<Left>', self.move_left)
        self.root.bind('<Right>', self.move_right)
        self.root.bind('<Down>', self.fall)
        self.root.bind('<Up>', self.rotate)
        self.root.bind('<space>', self.drop)
        self.refX = 3
        self.refY = -1
        self.ghosts = []
        self.drop_score = 0
        for b in self.blocks:
            if self.board.board[b.y][b.x].canvas["background"] != "black":
                self.death = True
            self.ghosts.append(Block(b.x, b.y))
        for i in range(20):
            if self.board.below_is_empty(self.ghosts):
                for g in self.ghosts:
                    g.y += 1
        self.draw(self.ghosts, "gray")
        self.draw(self.blocks, self.color)

    def draw(self, items, color):
        for i in items:
            self.board.board[i.y][i.x].canvas.config(bg=color)

    def fall(self, filler):
        if self.pause:
            pass
        elif self.board.below_is_empty(self.blocks):
            self.refY += 1
            self.draw(self.blocks, "black")
            for b in self.blocks:
                b.y += 1
            self.draw(self.blocks, self.color)
            if filler == "hard drop":
                self.drop_score += 2
            elif filler != "":
                self.drop_score += 1
        else:
            self.fallen = True

    def drop(self, filler):
        for i in range(20):
            self.fall("(Player input)")

    def ghost(self):
        self.draw(self.ghosts, "black")
        self.ghosts = []
        for b in self.blocks:
            self.ghosts.append(Block(b.x, b.y))
        for i in range(20):
            if self.board.below_is_empty(self.ghosts):
                for g in self.ghosts:
                    g.y += 1
        self.draw(self.ghosts, "gray")

    def move_left(self, filler):
        if self.pause:
            pass
        elif self.board.left_is_empty(self.blocks) and not self.fallen:
            self.refX -= 1
            self.draw(self.blocks, "black")
            for b in self.blocks:
                b.x -= 1
            self.ghost()
            self.draw(self.blocks, self.color)

    def move_right(self, filler):
        if self.pause:
            pass
        elif self.board.right_is_empty(self.blocks) and not self.fallen:
            self.refX += 1
            self.draw(self.blocks, "black")
            for b in self.blocks:
                b.x += 1
            self.ghost()
            self.draw(self.blocks, self.color)

    def rotate(self, filler):
        if self.pause:
            pass
        #default rotate
        elif self.board.check_rotate(self, self.blocks) and not self.fallen:
            for b in self.blocks:
                temp = b.y
                b.y = self.refY+b.x-self.refX
                b.x = self.refX+3-temp+self.refY
            self.ghost()
            self.draw(self.blocks, self.color)
        #rotate with kick right by 1
        elif self.board.check_rotate(self, self.blocks, 1, 0) and not self.fallen:
            for b in self.blocks:
                temp = b.y
                b.y = self.refY+b.x-self.refX
                b.x = self.refX+3-temp+self.refY + 1
            self.refX += 1
            self.ghost()
            self.draw(self.blocks, self.color)
        #rotate with kick left by 1
        elif self.board.check_rotate(self, self.blocks, -1, 0) and not self.fallen:
            for b in self.blocks:
                temp = b.y
                b.y = self.refY+b.x-self.refX
                b.x = self.refX+3-temp+self.refY - 1
            self.refX -= 1
            self.ghost()
            self.draw(self.blocks, self.color)


class TPiece(Piece):

    color = "purple"
    type = 0

    def __init__(self, root, board):
        self.b1 = Block(4, 0)
        self.b2 = Block(4, 1)
        self.b3 = Block(3, 1)
        self.b4 = Block(5, 1)
        self.blocks = self.ghosts = {self.b1, self.b2, self.b3, self.b4}
        Piece.__init__(self, root, board)


class OPiece(Piece):

    color = "yellow"
    type = 1

    def __init__(self, root, board):
        self.b1 = Block(4, 0)
        self.b2 = Block(4, 1)
        self.b3 = Block(5, 0)
        self.b4 = Block(5, 1)
        self.blocks = {self.b1, self.b2, self.b3, self.b4}
        Piece.__init__(self, root, board)


class IPiece(Piece):

    color = "aqua"
    type = 2

    def __init__(self, root, board):
        self.b1 = Block(3, 0)
        self.b2 = Block(4, 0)
        self.b3 = Block(5, 0)
        self.b4 = Block(6, 0)
        self.blocks = {self.b1, self.b2, self.b3, self.b4}
        Piece.__init__(self, root, board)


class ZPiece(Piece):

    color = "green"
    type = 3

    def __init__(self, root, board):
        self.b1 = Block(4, 0)
        self.b2 = Block(4, 1)
        self.b3 = Block(3, 0)
        self.b4 = Block(5, 1)
        self.blocks = {self.b1, self.b2, self.b3, self.b4}
        Piece.__init__(self, root, board)


class SPiece(Piece):

    color = "red"
    type = 4

    def __init__(self, root, board):
        self.b1 = Block(4, 0)
        self.b2 = Block(4, 1)
        self.b3 = Block(3, 1)
        self.b4 = Block(5, 0)
        self.blocks = {self.b1, self.b2, self.b3, self.b4}
        Piece.__init__(self, root, board)


class JPiece(Piece):

    color = "blue"
    type = 5

    def __init__(self, root, board):
        self.b1 = Block(3, 0)
        self.b2 = Block(3, 1)
        self.b3 = Block(4, 1)
        self.b4 = Block(5, 1)
        self.blocks = {self.b1, self.b2, self.b3, self.b4}
        Piece.__init__(self, root, board)


class LPiece(Piece):

    color = "orange"
    type = 6

    def __init__(self, root, board):
        self.b1 = Block(3, 1)
        self.b2 = Block(4, 1)
        self.b3 = Block(5, 1)
        self.b4 = Block(5, 0)
        self.blocks = {self.b1, self.b2, self.b3, self.b4}
        Piece.__init__(self, root, board)
