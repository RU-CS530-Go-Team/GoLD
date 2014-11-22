'''
Created on Oct 21, 2014

@author: JBlackmore
'''
from Tkinter import *

#from gold.models.Problem import Problem
from gold.models.board import Board
from gold.models.search import MinMaxTree

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
    board = Board(spaces, spaces)
    ovals = []
    C=None
    
    def __init__(self, dim_x, dim_y, margin, spaces):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.margin = margin
        self.spaces = spaces
        self.diam = (float(dim_x)-2*float(margin))/float(spaces-1)
        self.board = Board(spaces, spaces)
        self.master = Tk()
        self.C = Canvas(self.master, width=self.dim_x, height=self.dim_y, bg='#d8af4f')
        self.C.pack()
        self.drawGrid()
        def callback(event):
            self.placeStoneNear(event.x, event.y, 'white')
        def callback2(event):
            [i, j] = self.computeSpace(event.x, event.y)
            self.placeStoneNear(event.x, event.y, 'black')
            self.goForWhite(i, j)
        # Left-click for white, right-click for black
        self.C.bind("<Button-1>", callback2)
        #self.C.bind("<Button-3>", callback2)
        

    def goForWhite(self, pi, pj):
        tree = MinMaxTree(self.board, False, True, 0, 0.0, 'b({},{})'.format(pi,pj))
        [i, j] = tree.decideNextMove()
        self.board.place_stone(i, j, False)
        #print(self.board)
        self.drawBoard()

    def mainloop(self):        
        mainloop()
        
    def computeSpace(self, x_coord, y_coord):
        i = int(round((y_coord-self.margin)/self.diam))
        if( i<0 ):
            i=0
        elif( i>self.spaces-1 ):
            i = self.spaces - 1
        j = int(round((x_coord-self.margin)/self.diam))
        if( j<0 ):
            j=0
        elif( j>self.spaces-1 ):
            j = self.spaces - 1
        return [i, j]
    
    def computeCoord(self, i, j):
        y = self.margin+round((i)*self.diam) 
        x = self.margin + round((j)*self.diam)
        return [x, y]
    
    def placeStoneNear(self, x, y, color):
        [i, j] = self.computeSpace(x, y)
        #print("test.place_stone({},{}, {})".format(i,j, color=='black'))
        #if not self.board.board_spaces()[i][j] == '0':
        if (i,j) in self.board.white_stones+self.board.black_stones:
            print ("There's already a stone at ({}, {}).".format(i, j))
        else:
            self.board.place_stone(i, j, color=='black')
            #print(self.board)
            self.drawBoard()

    def drawStone(self, i, j, color):
        [x0, y0] = self.computeCoord(i, j)
        x1 = x0+self.diam/2 #10
        y1 = y0+self.diam/2 #10
        x0 = x0+1-self.diam/2 #9
        y0 = y0+1-self.diam/2
        self.ovals.append(self.C.create_oval(x0, y0, x1, y1, fill=color, tags=color))

    def drawPoint(self, i, j):
        [x0, y0] = self.computeCoord(i, j)
        x1 = x0+5
        y1 = y0+5
        x0 = x0-4
        y0 = y0-4
        self.ovals.append(self.C.create_oval(x0, y0, x1, y1, fill='black'))
    def setBoard(self, newboard):
        self.board = newboard
        
    def drawGrid(self):
        for i in range(self.spaces):
            self.C.create_line(self.margin, self.margin+i*self.diam, self.dim_x-self.margin, self.margin+i*self.diam)
            self.C.create_line(self.margin+i*self.diam, self.margin, self.margin+i*self.diam, self.dim_y-self.margin )
        self.drawPoint(3, 3)
        self.drawPoint(3, self.spaces-4)
        self.drawPoint(self.spaces-4, 3)
        self.drawPoint(self.spaces-4, self.spaces-4)
        self.drawPoint(3, (self.spaces-1)/2)
        self.drawPoint((self.spaces-1)/2, 3)
        self.drawPoint((self.spaces-1)/2, (self.spaces-1)/2)
        self.drawPoint(self.spaces-4, (self.spaces-1)/2)
        self.drawPoint((self.spaces-1)/2, self.spaces-4)

    ''' Draws board dim_x x dim_y pixels, with margin 'margin' 
        and number of spaces 'spaces'. Only tested with (400, 400, 12, 19).   
    ''' 
    def drawBoard(self): #board, dim_x, dim_y, diam, margin, spaces):
        #i = 0

        for c in self.C.children:
            c.destroy()
        #for oval in self.ovals:
        #    oval.destroy()
        self.C.delete('white')
        for white_stone in self.board.white_stones:
            self.drawStone(white_stone[0],white_stone[1], 'white')
        self.C.delete('black')
        for black_stone in self.board.black_stones:
            self.drawStone(black_stone[0],black_stone[1], 'black')
        #for row in self.board.board_spaces():
        #    j = 0 
        #    for space in row: 
        #        if space=='b': 
        #            self.drawStone(self.C, i, j, 'black')
        #        elif space=='w':
        #            self.drawStone(self.C, i, j, 'white')
        #        j = j + 1
        #    i = i + 1
    
#ui=Launcher(DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_MARGIN, DEFAULT_SPACES)
#ui=Launcher(DEFAULT_WIDTH, DEFAULT_HEIGHT, 30,5)
#ui.drawBoard()
'''
p1 = Problem('c:/users/jblackmore/Documents/Personal/Rutgers/530/gold/dataset/9286.sgf')
ui = Launcher(400,400,30,19)
mmt = MinMaxTree(p1.start, True, False, 0, 0.0)
print("Value={}".format(mmt.value))
ui.setBoard(p1.start)
ui.drawBoard()
ui.mainloop()
'''
ui = Launcher(400,400,50,5)
ui.drawBoard()
ui.mainloop()


