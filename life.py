# Maxwell Andrew
# Mar 23, 2015
# Game of Life

## Import Libraries ##

# use Tkinter GUI library
from Tkinter import *
# find file to load()
import tkFileDialog


## Variables ##

# visible colors
currGrid = []
# LIVE or DEAD
board = []
# wait to be set
row = 0
# wait to be set
col = 0
sqSize = 25
DEAD = 0
LIVE = 1
selected = None
beenHit = False


## Functions ##

def submit():
    global row
    global col
    row = int(rowE.get())
    col = int(colE.get())
    v.destroy()

def start():
    global beenHit
    global reInc
    # function has been used
    beenHit = True
    # step once through
    inc()
    # restep after 500 milliseconds
    reInc = w.after(500,start)

def pause():
    # cancel alarm to restep
    w.after_cancel(reInc)

def inc():
    global board
    boardcopy = [r[:] for r in board]
    for j in range(col):
        for i in range(row):
            # findNeigh(i,j) as int of neighbors to currGrid[i][j]
            if findNeigh(i,j) < 2:
                boardcopy[i][j] = DEAD
            elif findNeigh(i,j) == 2:
                pass
            elif findNeigh(i,j) == 3:
                boardcopy[i][j] = LIVE
            if findNeigh(i,j) > 3:
                boardcopy[i][j] = DEAD
    board = [r[:] for r in boardcopy]
    update()

def load():
    global source
    # remove LIVE tiles
    for m in range(col):
        for n in range(row):
            dead(m,n)
    s=tkFileDialog.askopenfilename(title='Select file',parent=w,filetypes=[('TXT','*.txt')])
    source.delete(0,END)
    source.insert(0,s)
    fname = source.get()
    config(fname)

def config(filename):
    if beenHit == True:
        pause()
    f = open(filename,'r')
    for line in f:
        parsed = line.split()
        if len(parsed)>1:
            y = int(parsed[0].strip())
            z = int(parsed[1].strip())
            alive(y,z)

def update():
    # ensure all LIVE blocks are green and DEAD white
    for m in range(col):
        for n in range(row):
            if board[n][m] == DEAD:
                dead(m,n)
            elif canvas.itemcget(currGrid[n][m], 'fill') == 'green' or board[n][m] == LIVE:
                alive(m,n)
            else:
                dead(m,n)

# x: col
def edgeX(x):
    if x >= col:
        x = 0
    if x < 0:
        x = col-1
    return x

# y: row
def edgeY(y):
    if y >= row:
        y = 0
    if y < 0:
        y = row-1
    return y

# return int of surrounding LIVE cells
# x: col | y: row
def findNeigh(x,y):
    global neighCount
    neighCount = 0
    # from top left work down then across
    for k in range(-1,2):
        for h in range(-1,2):
            a = x+h
            b = y+k
            # adjust for x and y overrun to create torus
            a = edgeY(a)
            b = edgeX(b)
            # don't count self
            if [h,k] != [0,0]:
                if board[a][b] == LIVE:
                    neighCount += 1
    return neighCount

def checkClick(event):
    global selected, mousex, mousey
    selCount = 0
    mousex = event.x
    mousey = event.y
    # <selected> as int id of cell starting with (1,) moving down col, then next row
    selected = canvas.find_closest(mousex,mousey)
    for m in range(row):
        for n in range(col):
            selCount += 1
            if selCount == selected[0]:
                # board on top
                # DEAD -> LIVE
                if board[m][n] == DEAD:
                    alive(n,m)
                # LIVE -> DEAD
                elif board[m][n] == LIVE:
                    dead(n,m)
    w.update()

def alive(x,y):
    # x and y inverted from row and col
    canvas.itemconfigure(currGrid[y][x], fill='green')
    board[y][x] = LIVE

def dead(x,y):
    # x and y inverted from row and col
    canvas.itemconfigure(currGrid[y][x], fill='white')
    board[y][x] = DEAD


## Define Dimensions of Row and Column ##

v = Tk()
v.title('R&C')

# row label & entry field
rowL = Label(v, text='Row:')
rowL.grid(row=0,column=0)
rowE = Entry(v,width=5)
rowE.pack()
rowE.grid(row=1,column=0)

# column label & entry field
colL = Label(v, text='Column:')
colL.grid(row=0,column=1)
colE = Entry(v,width=5)
colE.pack()
colE.grid(row=1,column=1) # add variable name

# submit button
subB = Button(v, text='Submit', command=submit)
subB.pack()
subB.grid(row=2,column=0,columnspan=2)

v.mainloop()

## Event Handler and Main Loop ##

# initialize game board
w = Tk()
w.title('Game of Life')

# dimensions of main window
canvas=Canvas(w,height=col*sqSize+1,width=row*sqSize+1,highlightthickness=0)
canvas.grid(row=0,columnspan=4)

# draw grids of squares
for i in range(row):
    board.append([])
    currGrid.append([])
    for j in range(col):
        board[i].append(0)
        currGrid[i].append(canvas.create_rectangle(i*sqSize,j*sqSize,(i+1)*sqSize,(j+1)*sqSize))

# start button
startB = Button(w, text='Start', command=start, width=10)
startB.pack()
startB.grid(row=1,column=0)

# pause button
pauseB = Button(w, text='Pause', command=pause, width=10)
pauseB.pack()
pauseB.grid(row=1,column=1)

# increment button
incB = Button(w, text='Increment', command=inc, width=10)
incB.pack()
incB.grid(row=1,column=2)

# load button
loadB = Button(w, text='Load', command=load, width=10)
loadB.pack()
loadB.grid(row=1,column=3)

# invisible entry box as reference for load()
source=Entry(w,width=0)

canvas.bind('<Button-1>',checkClick)

w.mainloop()
