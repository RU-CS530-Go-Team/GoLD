'''
Created on Oct 21, 2014

@author: JBlackmore
'''
from Tkinter import *
from gold.models.BoardStub import BoardStub

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 400
DEFAULT_MARGIN = 12
BOARD_SPACES = 19
diam = (float(DEFAULT_WIDTH)-2*float(DEFAULT_MARGIN))/float(BOARD_SPACES-1)

''' Places a stone of color 'color' on the 
    space nearest (x, y) on Canvas C. 
'''

def computeSpace(x_coord, y_coord):
    i = int(round((x_coord-DEFAULT_MARGIN)/diam))
    if( i<0 ):
        i=0
    elif( i>BOARD_SPACES-1 ):
        i = BOARD_SPACES - 1
    j = int(round((y_coord-DEFAULT_MARGIN)/diam))
    if( j<0 ):
        j=0
    elif( j>BOARD_SPACES-1 ):
        j = BOARD_SPACES - 1
    return [i, j]

def computeCoord(i, j):
    x = round((i)*diam)+(round(diam/2.0))+1
    y = round((j)*diam)+(round(diam/2.0))+1
    return [x, y]

def placeStoneNear(C, board, x, y, color):
    [i, j] = computeSpace(x, y)
    print("({},{}) is over space ({},{})".format(x,y,i,j))
    if not board.board_spaces[i][j] == '0':
        print ("There's already a stone at ({}, {}).".format(i, j))
    else:
        board.placeStone(i, j, color)
        redrawBoard(C, board)
    
def drawStone(C, i, j, color):
    [x0, y0] = computeCoord(i, j)
    x1 = x0+10
    y1 = y0+10
    x0 = x0-9
    y0 = y0-9
    C.create_oval(x0, y0, x1, y1, fill=color)
    
def redrawBoard(C, board):
    i = 0
    for row in board.board_spaces:
        j = 0 
        for space in row: 
            if space=='b': 
                drawStone(C, i, j, 'black')
            elif space=='w':
                drawStone(C, i, j, 'white')
            j = j + 1
        i = i + 1
    
                
''' Draws board dim_x x dim_y pixels, with margin 'margin' 
    and number of spaces 'spaces'. Only tested with (400, 400, 12, 19).   
''' 
def drawBoard(dim_x, dim_y, margin, spaces):
    
    master = Tk()
    boardPic = PhotoImage(file="go-board.gif")
    w = Canvas(master, width=dim_x, height=dim_y)
    w.pack()
    w.create_image(dim_x/2, dim_y/2, image=boardPic)
    board = BoardStub()
    redrawBoard(w, board)
    def callback(event):
        print "clicked at", event.x, event.y
        placeStoneNear(w, board, event.x, event.y, 'white')
    def callback2(event):
        print "rt-clicked at", event.x, event.y
        placeStoneNear(w, board, event.x, event.y, 'black')
    # Left-click for white, right-click for black
    w.bind("<Button-1>", callback)
    w.bind("<Button-3>", callback2)
    mainloop()

drawBoard(DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_MARGIN, BOARD_SPACES)
