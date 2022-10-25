from tkinter import *
from board import *
from PIL import ImageTk, Image
import random
import time


# Defining functions
# Reset function
def reset(filler):
    global root, board, points, piece, nextPiece, display_points, held, already_held, gameover, combo, level, lines
    pause("")
    try:
        gameover.destroy()
    except:
        pass
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
    combo = 0
    level = 0
    lines = 0
    update_points()


# Quit function
def quitgame(filler):
    global quit
    quit = True


# Pause function
def pause(filler):
    global piece, pauseLabel, pauseWindow, resetButton, quitButton
    if piece.pause:
        pauseWindow.destroy()
        pauseLabel.destroy()
        resetButton.destroy()
        quitButton.destroy()
    else:
        pauseWindow = Canvas(root, width=180, height=120, bg="gray", highlightbackground="gray")
        pauseWindow.place(x=287, y=275, anchor="center")
        pauseLabel = Label(root, text="<<Paused>>", bg="gray", fg="white", font=("Courier", 16))
        pauseLabel.place(x=287, y=240, anchor="center")
        resetButton = Label(root, text="<Reset>", bg="gray", fg="white", font=("Courier", 16))
        resetButton.bind("<Button-1>", reset)
        resetButton.place(x=287, y=275, anchor="center")
        quitButton = Label(root, text="<Quit>", bg="gray", fg="white", font=("Courier", 16))
        quitButton.bind("<Button-1>", quitgame)
        quitButton.place(x=287, y=300, anchor="center")
    piece.pause = not piece.pause


# Function for creating a new random piece
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


# Function for displaying the next piece
def preview(pieces):
    global prev, prevLine, ImgList
    prev.delete('img')
    for i in range(len(pieces)):
        prev.create_image(3, 72*i+38, anchor=NW, image=ImgList[pieces[i]], tags='img')
    prev.tag_raise(prevLine)


# Function for holding pieces
def hold(filler):
    global piece, ImgList, hold_display, held, nextPiece, already_held
    if already_held:
        return False
    already_held = True
    hold_display.delete('img')
    hold_display.create_image(3, 38, anchor=NW, image=ImgList[piece.type], tags='img')
    piece.draw(piece.blocks, "black")
    piece.draw(piece.shadows, "black")
    temp = piece.type
    piece = new_piece(held)
    held = temp
    preview(nextPiece)


# Function for updating the points display
def update_points():
    global points, display_points, highscore, display_high
    points_str = str(points)
    zeros = ""
    for i in range(6-len(points_str)):
        zeros += "0"
    points_str = zeros + points_str
    display_points.delete('score')
    display_points.create_text(50, 39, text=points_str, fill="lime", font=("Courier", 16), tags='score')
    display_points.grid(column=3, row=6, rowspan=3, padx=15)
    if highscore < points:
        highscore = points
        display_high.delete('score')
        display_high.create_text(50, 39, text=points_str, fill="lime", font=("Courier", 15), tags='score')
        display_high.grid(column=3, row=9, rowspan=3, padx=15)


# Function for updating the level display
def update_level():
    global level, display_level, root
    level_str = str(level)
    if len(level_str) == 1:
        level_str = "0" + level_str
    display_level.delete('level')
    display_level.create_text(50, 39, text=level_str, fill="lime", font=("Courier", 16), tags='level')
    display_level.grid(column=3, row=12, rowspan=3, padx=15)
    if level != 0:
        level_up = Label(root, text="Level: " + level_str, bg="gray", fg="white", font=("Courier", 16))
        level_up.place(x=287, y=275, anchor="center")
        root.update()
        time.sleep(1)
        level_up.destroy()


# Create a window, title it, adjust the size, and change the background color to gray
root = Tk()
root.title("Tetris")
root.geometry("550x700")
root.resizable(width=False, height=False)
root.config(bg="gray")
root.grid_columnconfigure(0, weight=1)

# Start Screen
# This was taken from stackoverflow. I tried something similar, but it didn't work and I don't understand why ;-;
# Update: I've learned about lambdas and I now understand why (yay)
var = IntVar()
start = Label(root, text="<<Click here to start>>", fg="lime", bg="black", font=("Courier", 16))
start.bind("<Button-1>", lambda f: var.set(1))
start.grid(column=0, row=1, sticky="EW")

control_txt = ("Controls: \n"
               "Arrow Keys to move\n"
               "Up Arrow to rotate\n"
               "Down Arrow to drop faster (soft drop)\n"
               "Spacebar to drop to bottom (hard drop)\n"
               "C to hold\n"
               "Esc to pause")
controls = Label(root, text="<<<Welcome to Tetris!>>>\n\n" + control_txt, fg="lime", bg="black", font=("Courier", 16))
controls.grid(column=0, row=0, sticky="EW", pady=(230, 0))

# Clear the screen
start.wait_variable(var)
for w in root.winfo_children():
    w.destroy()


# Start of actual game code

# Binding keys to the appropriate functions
# (just pausing and holding bc i put the reset and quit functions into the pause menu)
root.bind('<Escape>', pause)
root.bind('c', hold)

# Create a board with the board object
board = Board(root)

# Initialize the points and display them
combo = 0
points = 0
display_points = Canvas(root, width=96, height=58, bg="black", highlightbackground="lime")
display_points.create_text(52, 10, text="Points:", fill="lime", anchor="center", font=("Courier", 16))
highscore = 0
display_high = Canvas(root, width=96, height=58, bg="black", highlightbackground="lime")
display_high.create_text(52, 10, text="Highscore:", fill="lime", anchor="center", font=("Courier", 15))
display_high.create_text(50, 39, text="000000", fill="lime", font=("Courier", 16), tags='score')
display_high.grid(column=3, row=9, rowspan=3, padx=15)
update_points()

# Create starting piece and initialize the list of next pieces
nextPiece = [random.randint(0, 6),
             random.randint(0, 6)]
piece = new_piece()

# Initializing a list of piece images to help with the preview and hold display
ImgList = [ImageTk.PhotoImage(Image.open("Previews/TPiece.png").resize((96, 72))),
           ImageTk.PhotoImage(Image.open("Previews/OPiece.png").resize((96, 72))),
           ImageTk.PhotoImage(Image.open("Previews/IPiece.png").resize((96, 72))),
           ImageTk.PhotoImage(Image.open("Previews/ZPiece.png").resize((96, 72))),
           ImageTk.PhotoImage(Image.open("Previews/SPiece.png").resize((96, 72))),
           ImageTk.PhotoImage(Image.open("Previews/JPiece.png").resize((96, 72))),
           ImageTk.PhotoImage(Image.open("Previews/LPiece.png").resize((96, 72)))]

# Creating the preview gui and displaying the next pieces
prev = Canvas(root, width=96, height=182, bg="black", highlightbackground="lime")
prev.create_text(48, 10, text="Next:", fill="lime", font=("Courier", 16))
prevLine = prev.create_line(0, 110, 100, 110, fill="lime", width=3)
prev.grid(row=1, column=27, rowspan=8, columnspan=4, padx=15)
preview(nextPiece)

# Creating the held piece gui
hold_display = Canvas(root, width=96, height=110, bg="black", highlightbackground="lime")
hold_display.create_text(48, 10, text="Held:", fill="lime", font=("Courier", 16))
hold_display.grid(row=1, column=3, rowspan=5, columnspan=4, padx=15)
held = -1  # -1 means no specific type, so nothing is held
already_held = False

# Display the controls in case the user needs a reminder or neglected to read them
controls = Label(root, text=control_txt, fg="lime", bg="black", font=("Courier", 16))
controls.place(relx=0.5, y=610, anchor="center")

# Initializing variables for the level and displaying it
level = 0
level_speeds = [6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2]
lines = 0  # Thank you so much for letting me fix this (sorry)
display_level = Canvas(root, width=96, height=58, bg="black", highlightbackground="lime")
display_level.create_text(52, 10, text="Level:", fill="lime", font=("Courier", 16))
update_level()

# Using variables to set "gravity"
fall_timer = 0
fall_speed = 48-level*5

# Main loop
quit = False
while not quit:
    # Make sure to award points for soft dropping or hard dropping
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
        # Reset fall timer
        fall_timer = 0
        # Allow the player to hold the next piece
        already_held = False
        # Clear the necessary lines and calculate points to give
        # Points are determined based on the amount of lines cleared at once, the level, and any combo the player has
        # (I haven't included extra points for difficult spins/clears bc idk how)
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
        # Check to see if the level should advance and do it if needed
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
            update_level()
        # Once the piece has fallen, create a new piece and preview the next piece
        piece = new_piece()
        preview(nextPiece)
        # If the new piece would cause a death (the spawn overlaps with an existing piece), the game is over
        if piece.death:
            # Game over screen
            var = IntVar()
            pause("")
            gameover = Label(root, text="<<<GAME OVER>>>\nScore: %d" % points, fg="white", bg="gray", font=("Courier", 16))
            gameover.place(x=287, y=240, anchor="center")
    # add a delay to the update speed (acts as frames per second as well as tick rate)
    time.sleep(1/60)
    fall_timer += 1
    # update the screen
    root.update()