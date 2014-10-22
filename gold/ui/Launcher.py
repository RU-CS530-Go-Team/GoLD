'''
Created on Oct 21, 2014

@author: JBlackmore
'''
from Tkinter import *

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 400
DEFAULT_MARGIN = 12
BOARD_SPACES = 19

''' Places a stone of color 'color' on the 
    space nearest (x, y) on Canvas C. 
'''
def placeStoneNear(C, x, y, color):
    diam = (float(DEFAULT_WIDTH)-2*float(DEFAULT_MARGIN))/float(BOARD_SPACES-1)
    x0 = round(round((x-DEFAULT_MARGIN)/diam)*diam)+2
    x1 = x0+round(diam)-2
    y0 = round(round((y-DEFAULT_MARGIN)/diam)*diam)+2
    y1 = y0+round(diam)-2
    C.create_oval(x0, y0, x1, y1, fill=color)

''' Draws board dim_x x dim_y pixels, with margin 'margin' 
    and number of spaces 'spaces'. Only tested with (400, 400, 12, 19).   
''' 
def drawBoard(dim_x, dim_y, margin, spaces):
    
    master = Tk()
    boardPic = PhotoImage(file="go-board.gif")
    w = Canvas(master, width=dim_x, height=dim_y)
    w.pack()
    w.create_image(dim_x/2, dim_y/2, image=boardPic)
    def callback(event):
        print "clicked at", event.x, event.y
        placeStoneNear(w, event.x, event.y, 'white')
    def callback2(event):
        print "rt-clicked at", event.x, event.y
        placeStoneNear(w, event.x, event.y, 'black')
    # Left-click for white, right-click for black
    w.bind("<Button-1>", callback)
    w.bind("<Button-3>", callback2)
    mainloop()

drawBoard(DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_MARGIN, BOARD_SPACES)
