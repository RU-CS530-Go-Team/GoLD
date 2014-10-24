'''
Created on Oct 21, 2014

@author: JBlackmore
'''
from Tkinter import *
from gold.models.board import Board

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 400
DEFAULT_MARGIN = 12
DEFAULT_SPACES = 19

''' Places a stone of color 'color' on the 
    space nearest (x, y) on Canvas C. 
'''
class Launcher:
    dim_x = DEFAULT_WIDTH
    dim_y = DEFAULT_WIDTH
    margin = DEFAULT_MARGIN
    spaces = DEFAULT_SPACES
    diam = (float(dim_x)-2*float(margin))/float(spaces-1)
    board = Board(dim_x, dim_y)
    
    def __init__(self, dim_x, dim_y, margin, spaces):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.margin = margin
        self.spaces = spaces
        self.diam = (float(dim_x)-2*float(margin))/float(spaces-1)
        self.board = Board(dim_x, dim_y)
        self.master = Tk()
        self.C = None
        #self.C = Canvas(self.master, width=self.dim_x, height=self.dim_y, bg='#d8af4f')

    def computeSpace(self, x_coord, y_coord):
        i = int(round((x_coord-self.margin)/self.diam))
        if( i<0 ):
            i=0
        elif( i>self.spaces-1 ):
            i = self.spaces - 1
        j = int(round((y_coord-self.margin)/self.diam))
        if( j<0 ):
            j=0
        elif( j>self.spaces-1 ):
            j = self.spaces - 1
        return [i, j]
    
    def computeCoord(self, i, j):
        x = self.margin+round((i)*self.diam) #+(round(diam/2.0))+1
        y = self.margin + round((j)*self.diam) #+(round(diam/2.0))+1
        return [x, y]
    
    def placeStoneNear(self, C, x, y, color):
        [i, j] = self.computeSpace(x, y)
        print("({},{}) is over space ({},{})".format(x,y,i,j))
        if not self.board.board_spaces()[i][j] == '0':
            print ("There's already a stone at ({}, {}).".format(i, j))
        else:
            self.board.place_stone(i, j, color=='black')
            self.drawBoard()

    def drawStone(self, C, i, j, color):
        [x0, y0] = self.computeCoord(i, j)
        print("Drawing stone ({},{}) at coordinates ({},{})".format(i,j,x0,y0))
        x1 = x0+self.diam/2 #10
        y1 = y0+self.diam/2 #10
        x0 = x0+1-self.diam/2 #9
        y0 = y0+1-self.diam/2
        C.create_oval(x0, y0, x1, y1, fill=color)

    def drawPoint(self, C, i, j):
        [x0, y0] = self.computeCoord(i, j)
        x1 = x0+5
        y1 = y0+5
        x0 = x0-4
        y0 = y0-4
        C.create_oval(x0, y0, x1, y1, fill='black')
        
    def drawGrid(self):
        print("self.diam={}".format(self.diam))
        for i in range(self.spaces):
            self.C.create_line(self.margin, self.margin+i*self.diam, self.dim_x-self.margin, self.margin+i*self.diam)
            self.C.create_line(self.margin+i*self.diam, self.margin, self.margin+i*self.diam, self.dim_y-self.margin )
        self.drawPoint(self.C, 3, 3)
        self.drawPoint(self.C, 3, self.spaces-4)
        self.drawPoint(self.C, self.spaces-4, 3)
        self.drawPoint(self.C, self.spaces-4, self.spaces-4)
        self.drawPoint(self.C, 3, (self.spaces-1)/2)
        self.drawPoint(self.C, (self.spaces-1)/2, 3)
        self.drawPoint(self.C, (self.spaces-1)/2, (self.spaces-1)/2)
        self.drawPoint(self.C, self.spaces-4, (self.spaces-1)/2)
        self.drawPoint(self.C, (self.spaces-1)/2, self.spaces-4)

    ''' Draws board dim_x x dim_y pixels, with margin 'margin' 
        and number of spaces 'spaces'. Only tested with (400, 400, 12, 19).   
    ''' 
    #def drawBoard(self, dim_x, dim_y, margin, spaces):
        
        #master = Tk()
        #diam = (float(dim_x)-2*float(margin))/float(spaces-1)
        #print ('{}-2x{}/{} = {}'.format(dim_x, margin, spaces-1, diam))
        #C = Canvas(master, width=dim_x, height=dim_y, bg='#d8af4f')
        #C.pack()
        #drawGrid(C, dim_x, dim_y, diam, margin, spaces)
        #board = Board(dim_x, dim_y)
#        self.redrawBoard()

    def drawBoard(self): #board, dim_x, dim_y, diam, margin, spaces):
        #board = Board(dim_x, self.dim_y)
        #redrawBoard(C, board, diam, margin)
        if self.C:
            self.C.destroy()
        self.C = Canvas(self.master, width=self.dim_x, height=self.dim_y, bg='#d8af4f')
        self.C.pack()
        #self.C =Canvas(self.master, width=self.dim_x, height=self.dim_y, bg='#d8af4f')
        self.drawGrid()
        # bg='#d8af4f'
        i = 0
        for row in self.board.board_spaces():
            j = 0 
            for space in row: 
                if space=='b': 
                    self.drawStone(self.C, i, j, 'black')
                elif space=='w':
                    self.drawStone(self.C, i, j, 'white')
                j = j + 1
            i = i + 1
        def callback(event):
            print "clicked at", event.x, event.y
            self.placeStoneNear(self.C, event.x, event.y, 'white')
        def callback2(event):
            print "rt-clicked at", event.x, event.y
            self.placeStoneNear(self.C, event.x, event.y, 'black')
        # Left-click for white, right-click for black
        self.C.bind("<Button-1>", callback)
        self.C.bind("<Button-3>", callback2)
        mainloop()
    
ui=Launcher(DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_MARGIN, DEFAULT_SPACES)
#ui=Launcher(DEFAULT_WIDTH, DEFAULT_HEIGHT, 35,9)
ui.drawBoard()
#drawBoard(500,500, 65, 7)
