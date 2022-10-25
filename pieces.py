class Block:

    # Constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Piece:

    # Constructor: initializes a bunch of variables
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
        self.shadows = []
        self.drop_score = 0
        # Check to see if the piece would cause a death
        for b in self.blocks:
            if self.board.board[b.y][b.x].canvas["background"] != "black":
                self.death = True
        # Create and draw the shadow
        self.shadow()
        # Draw the blocks
        self.draw(self.blocks, self.color)

    # Draw a set of blocks (used for the actual blocks and the shadow blocks)
    def draw(self, items, color):
        for i in items:
            self.board.board[i.y][i.x].canvas.config(bg=color)

    # Make the piece fall by 1 cell (also serves as the function for soft dropping)
    def fall(self, filler):
        # Make sure the game isn't paused
        if self.pause:
            pass
        # Fall if possible
        elif self.board.below_is_empty(self.blocks):
            self.refY += 1
            self.draw(self.blocks, "black")
            for b in self.blocks:
                b.y += 1
            self.draw(self.blocks, self.color)
            if filler == "hard drop":  # Reward 2 points per cell if hard dropped
                self.drop_score += 2
            elif filler != "":  # Reward 1 point per cell if soft dropped
                self.drop_score += 1
        # If not possible, make self.fallen True
        else:
            self.fallen = True

    # Hard drop the piece (fall 20 times)
    def drop(self, filler):
        for i in range(20):
            self.fall("hard drop")
            # This string differentiates the hard drop due to a player input from falling due to gravity

    # Find the coordinates of the shadow and draw it
    def shadow(self):
        self.draw(self.shadows, "black")
        self.shadows = []
        for b in self.blocks:
            self.shadows.append(Block(b.x, b.y))
        for i in range(20):
            if self.board.below_is_empty(self.shadows):
                for s in self.shadows:
                    s.y += 1
        self.draw(self.shadows, "gray")

    # Try to move the piece to the left
    def move_left(self, filler):
        # Make sure the game isn't paused
        if self.pause:
            pass
        # Move left if possible
        elif self.board.left_is_empty(self.blocks) and not self.fallen:
            self.refX -= 1
            self.draw(self.blocks, "black")
            for b in self.blocks:
                b.x -= 1
            self.shadow()
            self.draw(self.blocks, self.color)

    # Try to move the piece to the right
    def move_right(self, filler):
        # Make sure the game isn't paused
        if self.pause:
            pass
        # Move right if possible
        elif self.board.right_is_empty(self.blocks) and not self.fallen:
            self.refX += 1
            self.draw(self.blocks, "black")
            for b in self.blocks:
                b.x += 1
            self.shadow()
            self.draw(self.blocks, self.color)

    # Try to rotate the piece
    def rotate(self, filler):
        # Make sure the game isn't paused
        if self.pause:
            pass
        # Try default rotate
        else:
            # Make a list of possible offsets (x, y)
            try_rotate = [[0, 0], [1, 0], [-1, 0], [2, 0], [-2, 0],
                          [0, 1], [1, 1], [-1, 1], [2, 1], [-2, 1],
                          [0, 2], [1, 2], [-1, 2], [2, 2], [-2, 2]]
            # Go through the offsets until one works
            for n in try_rotate:
                if self.board.check_rotate(self, self.blocks, n[0], n[1]) and not self.fallen:
                    for b in self.blocks:
                        temp = b.y
                        b.y = self.refY + b.x - self.refX + n[1]
                        b.x = self.refX + 3 - temp + self.refY + n[0]
                    self.refX += n[0]
                    self.refY += n[1]
                    self.shadow()
                    self.draw(self.blocks, self.color)
                    return ""

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
