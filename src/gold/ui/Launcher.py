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
#diam = (float(DEFAULT_WIDTH)-2*float(DEFAULT_MARGIN))/float(BOARD_SPACES-1)

''' Places a stone of color 'color' on the 
    space nearest (x, y) on Canvas C. 
'''

def computeSpace(x_coord, y_coord, diam, margin):
    i = int(round((x_coord-margin)/diam))
    if( i<0 ):
        i=0
    elif( i>BOARD_SPACES-1 ):
        i = BOARD_SPACES - 1
    j = int(round((y_coord-margin)/diam))
    if( j<0 ):
        j=0
    elif( j>BOARD_SPACES-1 ):
        j = BOARD_SPACES - 1
    return [i, j]

def computeCoord(i, j, diam, margin):
    x = margin+round((i)*diam) #+(round(diam/2.0))+1
    y = margin + round((j)*diam) #+(round(diam/2.0))+1
    return [x, y]

def placeStoneNear(C, board, diam, margin, x, y, color):
    [i, j] = computeSpace(x, y, diam, margin)
    print("({},{}) is over space ({},{})".format(x,y,i,j))
    if not board.board_spaces[i][j] == '0':
        print ("There's already a stone at ({}, {}).".format(i, j))
    else:
        board.placeStone(i, j, color)
        redrawBoard(C, board, diam, margin)
    
def drawStone(C, i, j, diam, margin, color):
    [x0, y0] = computeCoord(i, j, diam, margin)
    print("Drawing stone ({},{}) at coordinates ({},{})".format(i,j,x0,y0))
    x1 = x0+diam/2 #10
    y1 = y0+diam/2 #10
    x0 = x0+1-diam/2 #9
    y0 = y0+1-diam/2
    C.create_oval(x0, y0, x1, y1, fill=color)

def drawPoint(C, i, j, diam, margin):
    [x0, y0] = computeCoord(i, j, diam, margin)
    x1 = x0+5
    y1 = y0+5
    x0 = x0-4
    y0 = y0-4
    C.create_oval(x0, y0, x1, y1, fill='black')
    
def redrawBoard(C, board, diam, margin):
    i = 0
    for row in board.board_spaces:
        j = 0 
        for space in row: 
            if space=='b': 
                drawStone(C, i, j, diam, margin, 'black')
            elif space=='w':
                drawStone(C, i, j, diam, margin, 'white')
            j = j + 1
        i = i + 1

def drawGrid(C, w, h, diam, margin, spaces):
    print("diam={}".format(diam))
    for i in range(spaces):
        C.create_line(margin, margin+i*diam, w-margin, margin+i*diam)
        C.create_line(margin+i*diam, margin, margin+i*diam, h-margin )
    drawPoint(C, 3, 3, diam, margin)
    drawPoint(C, 3, spaces-4, diam, margin)
    drawPoint(C, spaces-4, 3, diam, margin)
    drawPoint(C, spaces-4, spaces-4, diam, margin)
    drawPoint(C, 3, (spaces-1)/2, diam, margin)
    drawPoint(C, (spaces-1)/2, 3, diam, margin)
    drawPoint(C, (spaces-1)/2, (spaces-1)/2, diam, margin)
    drawPoint(C, spaces-4, (spaces-1)/2, diam, margin)
    drawPoint(C, (spaces-1)/2, spaces-4, diam, margin)
    
''' Draws board dim_x x dim_y pixels, with margin 'margin' 
    and number of spaces 'spaces'. Only tested with (400, 400, 12, 19).   
''' 
def drawBoard(dim_x, dim_y, margin, spaces):
    
    master = Tk()
    diam = (float(dim_x)-2*float(margin))/float(spaces-1)
    print ('{}-2x{}/{} = {}'.format(dim_x, margin, spaces-1, diam))
    C = Canvas(master, width=dim_x, height=dim_y, bg='#d8af4f')
    C.pack()
    drawGrid(C, dim_x, dim_y, diam, margin, spaces)
    board = BoardStub()
    redrawBoard(C, board, diam, margin)
    def callback(event):
        print "clicked at", event.x, event.y
        placeStoneNear(C, board, diam, margin, event.x, event.y, 'white')
    def callback2(event):
        print "rt-clicked at", event.x, event.y
        placeStoneNear(C, board, diam, margin, event.x, event.y, 'black')
    # Left-click for white, right-click for black
    C.bind("<Button-1>", callback)
    C.bind("<Button-3>", callback2)
    mainloop()

#drawBoard(DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_MARGIN, BOARD_SPACES)
drawBoard(DEFAULT_WIDTH, DEFAULT_HEIGHT, 35,9)
#drawBoard(500,500, 65, 7)
