from tkinter import *
from board import *
from PIL import ImageTk, Image
import random
import time


# defining functions
# reset function
def reset(filler):
    global root, board, points, piece, nextPiece, display_points, pauseLabel, held, already_held
    # wipe board
    for i in range(20):
        board.clear_line(i)
    piece = new_piece()
    nextPiece = [random.randint(0, 6),
                 random.randint(0, 6)]
    preview(nextPiece)
    hold_display.delete('img')
    already_held = False
    points = 0
    update_points()
    pauseLabel.destroy()
    piece.pause = False


# quit function
def quit(filler):
    global quit
    quit = True


# pause function
def pause(filler):
    global piece, pauseLabel
    if piece.pause:
        pauseLabel.destroy()
    else:
        pauseLabel = Label(root, text="<<Paused>>", bg="gray", fg="white")
        pauseLabel.place(x=286, y=240, anchor="center")
    piece.pause = not piece.pause


# function for creating a new random piece
def new_piece(type=-1):
    global root, board, nextPiece
    if type == -1:
        type = nextPiece[0]
        for i in range(len(nextPiece)-1):
            nextPiece[i] = nextPiece[i+1]
        nextPiece[-1] = random.randint(0, 6)
    if type == 0: return TPiece(root, board)
    if type == 1: return OPiece(root, board)
    if type == 2: return IPiece(root, board)
    if type == 3: return ZPiece(root, board)
    if type == 4: return SPiece(root, board)
    if type == 5: return JPiece(root, board)
    return LPiece(root, board)


# function for displaying the next piece
def preview(pieces):
    global prev, prevLine, ImgList
    prev.delete('img')
    for i in range(len(pieces)):
        prev.create_image(3, 72*i+38, anchor=NW, image=ImgList[pieces[i]], tags='img')
    prev.tag_raise(prevLine)


# function for holding pieces
def hold(filler):
    global piece, ImgList, hold_display, held, nextPiece, already_held
    if already_held:
        return False
    already_held = True
    hold_display.delete('img')
    hold_display.create_image(3, 38, anchor=NW, image=ImgList[piece.type], tags='img')
    piece.draw(piece.blocks, "black")
    piece.draw(piece.ghosts, "black")
    temp = piece.type
    piece = new_piece(held)
    held = temp
    preview(nextPiece)


def update_points():
    global points, display_points
    points_str = str(points)
    zeros = ""
    for i in range(6-len(points_str)):
        zeros += "0"
    points_str = zeros + points_str
    display_points.delete('score')
    display_points.create_text(50, 39, text=points_str, fill="lime", font=("Courier", 16), tags='score')
    display_points.grid(column=3, row=7, rowspan=3, padx=15)


# create a window, title it, adjust the size, and change the background color to gray
root = Tk()
root.title("Tetris")
root.geometry("550x700")
root.resizable(width=False, height=False)
root.config(bg="gray")
root.grid_columnconfigure(0, weight=1)

# Start Screen
# This was taken from stackoverflow. I tried something similar, but it didn't work and I don't understand why ;-;
var = IntVar()
start = Label(root, text="<<Press to start>>", fg="lime", bg="black", font=("Courier", 16))
start.bind("<Button-1>", lambda f: var.set(1))
start.grid(column=0, row=1, sticky="EW")

control_txt = ("Controls: \n"
               "Arrow Keys to move\n"
               "Up Arrow to rotate\n"
               "Down Arrow to drop faster (soft drop)\n"
               "Spacebar to drop to bottom (hard drop)\n"
               "C to hold\n"
               "R to reset\n"
               "Q to quit\n"
               "P to pause")
controls = Label(root, text="<<<Welcome to Tetris!>>>\n\n" + control_txt, fg="lime", bg="black", font=("Courier", 16))
controls.grid(column=0, row=0, sticky="EW")

start.wait_variable(var)
for w in root.winfo_children():
    w.destroy()

# start of actual game code

# binding keys to the appropriate functions
root.bind('r', reset)
root.bind('q', quit)
root.bind('p', pause)
root.bind('c', hold)

# Create a board with the board object, then initialize the points and display them
board = Board(root)
points = 0
combo = 0
display_points = Canvas(root, width=96, height=58, bg="black", highlightbackground="lime")
display_points.create_text(52, 10, text="Points:", fill="lime", font=("Courier", 16))
update_points()

# Create starting piece and initialize the list of next pieces
nextPiece = [random.randint(0, 6),
             random.randint(0, 6)]
piece = new_piece()

# Setting a variable for the next piece and initializing a list to be used for displaying the preview
ImgList = [ImageTk.PhotoImage(Image.open("Previews/TPiece.png").resize((96, 72))),
           ImageTk.PhotoImage(Image.open("Previews/OPiece.png").resize((96, 72))),
           ImageTk.PhotoImage(Image.open("Previews/IPiece.png").resize((96, 72))),
           ImageTk.PhotoImage(Image.open("Previews/ZPiece.png").resize((96, 72))),
           ImageTk.PhotoImage(Image.open("Previews/SPiece.png").resize((96, 72))),
           ImageTk.PhotoImage(Image.open("Previews/JPiece.png").resize((96, 72))),
           ImageTk.PhotoImage(Image.open("Previews/LPiece.png").resize((96, 72)))]
prev = Canvas(root, width=96, height=182, bg="black", highlightbackground="lime")
prev.create_text(48, 10, text="Next:", fill="lime", font=("Courier", 16))
prevLine = prev.create_line(0, 110, 100, 110, fill="lime", width=3)
prev.grid(row=1, column=27, rowspan=8, columnspan=4, padx=15)
preview(nextPiece)

# initializing for the hold function and displaying the held piece box
hold_display = Canvas(root, width=96, height=110, bg="black", highlightbackground="lime")
hold_display.create_text(48, 10, text="Held:", fill="lime", font=("Courier", 16))
hold_display.grid(row=1, column=3, rowspan=5, columnspan=4, padx=15)
held = -1  # -1 means no specific type, so nothing is held
already_held = False

# display controls in case the user needs a reminder or neglected to read them
controls = Label(root, text=control_txt, fg="lime", bg="black", font=("Courier", 16))
controls.place(relx=0.5, y=610, anchor="center")

# Initializing variables for the level
level = 0
level_speeds = [6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2]
lines = 0
print("Level: %d" % level)

# Using variables to set "gravity"
fall_timer = 0
fall_speed = 48-level*5

# Main loop
quit = False
while not quit:
    points += piece.drop_score
    if piece.drop_score != 0:
        update_points()
        piece.drop_score = 0
    # Fall timer
    if fall_timer == fall_speed:
        fall_timer = 0
        if not piece.pause:
            piece.fall("")
    # Once the piece has fallen, check to see if a line is full. If so, clear that line and add 1000 points
    if piece.fallen:
        # allow the player to hold the next piece
        already_held = False
        # clear lines and calculate points to give
        cleared = 0
        for i in range(20):
            if board.line_is_full(i):
                board.clear_line(i)
                lines += 1
                cleared += 1
        if cleared == 4:
            combo += 1
            points += 800*level
        elif cleared != 0:
            combo += 1
            points += (cleared*200 - 100)*level
            points += 50*combo*level
        else:
            combo = 0
        update_points()
        # check to see if the level should advance
        if lines >= (level+1)*10 and level != 29:
            level += 1
            fall_timer = 0
            if level < 9:
                fall_speed = 48-level*5
            elif level < 19:
                fall_speed = level_speeds[level-9]
            elif level < 29:
                fall_speed = 2
            else:
                fall_speed = 1
            print("Level: %d" % level)
        # Once the piece has fallen, create a new piece
        piece = new_piece()
        preview(nextPiece)
        # If the new piece would cause a death, end the main loop (leads to game over screen)
        if piece.death:
            # Game over screen
            var = IntVar()
            pause("")
            gameover = Label(root, text="<<<GAME OVER>>>\nScore: %d" % points, fg="lime", bg="black", font=("Courier", 16))
            gameover.place(x=286, y=240, anchor="center")
    # add a delay to the update speed (acts as frames per second as well as tick rate)
    time.sleep(1/60)
    fall_timer += 1
    # update the screen
    root.update()