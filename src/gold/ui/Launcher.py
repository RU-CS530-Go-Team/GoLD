'''
Created on Oct 21, 2014

@author: JBlackmore
'''
#from Tkinter import *
from Tkinter import *
#from gold.models.Problem import Problem
from gold.models.board import Board, IllegalMove
#from gold.models.search import MinMaxTree
from gold.extraneous.life import determineLife
from gold.extraneous.MoveTreeParser import MoveTreeParser
from gold.learn.trainer import FeatureExtractor

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 400
DEFAULT_MARGIN = 12
DEFAULT_SPACES = 19

''' Places a stone of color 'color' on the
    space nearest (x, y) on Canvas C.
'''
class ResizingCanvas(Canvas):
    def __init__(self, parent, launcher, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.parent=parent
        self.bind('<Configure>', self.on_resize)
        self.launcher = launcher
        
    def on_resize(self, event):
        self.parent.update()
        #geo = self.parent.geometry()
        print('-{},{}'.format(event.width, event.height))
        self.width = self.parent.winfo_width()
        self.height = self.parent.winfo_height()-42 # for the title bar I guess
        #self.width=event.width
        #self.height=event.height
        #self.config(width=self.width, height=self.height)
        print(self.width, self.height)
        self.launcher.resize(self.width, self.height)
        
class Launcher:
    def __init__(self, dim_x, dim_y, margin, spaces, board=None):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.margin = margin
        self.spaces = spaces
        self.ovals=[]
        if board==None:
            self.board = Board(spaces, spaces)
        else:
            self.board = board
            self.spaces = max(board.x, board.y)
        self.diam = (float(dim_x)-2*float(margin))/float(self.spaces-1)
        self.master = Tk()
        self.master.resizable(True, True)
        self.board_frame = Frame(width=self.dim_x, height=dim_y, bg='#d8af4f')
        self.board_frame.pack(side=TOP, fill=BOTH, expand=YES)
        #self.scaler_frame =Frame(width=self.dim_x, height=42, bg='#d8af4f')
        #self.scaler_frame.pack(side=BOTTOM, fill=X, expand=YES)
        self.C = None
        self.drawGrid()
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        def callback(event):
            #[i, j] = self.computeSpace(event.x, event.y)
            self.placeStoneNear(event.x, event.y, 'white')
        def callback2(event):
            #[i, j] = self.computeSpace(event.x, event.y)
            self.placeStoneNear(event.x, event.y, 'black')
            #self.goForWhite(i, j)
        # Left-click for white, right-click for black
        self.C.bind("<Button-1>", callback2)
        self.C.bind("<Button-3>", callback)

    def resize(self, x, y):
        if x==self.dim_x and y==self.dim_y:
            return
        self.dim_x = x
        self.dim_y = y
        #self.ovals=[]
        self.diam = (float(min(x,y))-2*float(self.margin))/float(self.spaces-1)
        #self.master = Tk()
        
        #self.C.destroy()
        #self.C = ResizingCanvas(self.board_frame, self, width=self.dim_x, height=self.dim_y, bg='#d8af4f')
        #self.C.pack(side=TOP, fill=BOTH, expand=YES)
        self.drawGrid()
        self.drawBoard()
        
    def goForWhite(self, pi, pj):
        #tree = MinMaxTree(self.board, False, True, 0, 0.0, 'b({},{})'.format(pi,pj))
        #bestMove = tree.decideNextMove()
        
        #self.board.place_stone(bestMove.i, bestMove.j, False)
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

    def drawStone(self, i, j, color, alive=False):
        [x0, y0] = self.computeCoord(i, j)
        x2 = x0+self.diam/2 #10
        y2 = y0+self.diam/2 #10
        x1 = x0+1-self.diam/2 #9
        y1 = y0+1-self.diam/2
        
        self.ovals.append(self.C.create_oval(x1, y1, x2, y2, fill=color, tags=color))
        if( alive ):
            self.ovals.append(self.C.create_oval(x0-2, y0-2, x0+1, y0+1, fill='green', tags=color))
    def setBoardIndex(self, index):
        self.setBoard(self.boards[int(index)-1])
        self.drawBoard()
        
    def showPath(self, boards):
        self.boards = boards
        scale = Scale(self.master, orient=HORIZONTAL, from_=1, to=len(boards), command=self.setBoardIndex)
        scale.pack(side=BOTTOM)
        self.setBoard(boards[0])
        self.drawBoard()
        self.mainloop()
        
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
        if self.C is None:
            #self.C.destroy()
            self.C = ResizingCanvas(self.board_frame, self, width=self.dim_x, height=self.dim_y, highlightthickness=0, bg='#d8af4f')
            #self.C.grid(row=0,column=0, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)
        
        self.C.pack(side=TOP, fill=BOTH, expand=YES)
        self.C.delete(ALL)
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
        for [color,stones] in [['white', self.board.white_stones], ['black', self.board.black_stones]]:
            living_groups = determineLife(self.board, color)
            self.C.delete(color)
            for stone in stones:
                alive = False
                for group in living_groups:
                    if not alive and stone in group:
                        alive = True
                self.drawStone(stone[0],stone[1],color,alive)
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
def load_problem_start(f):
    mtp = MoveTreeParser(f)
    return mtp.start

def load_problem_paths(f):
    mtp = MoveTreeParser(f)
    #print('{} := {}'.format(f.split('/')[-1].split('\\')[-1], mtp.problemType))
    sn = mtp.getSolutionNodes()
    inc = mtp.getIncorrectNodes()
    probtyp = mtp.getProblemType()
    if probtyp == 1 or probtyp == 3: #Black to live
        probtyp = 1
    elif probtyp == 2 or probtyp == 4: #White to kill
        probtyp = 2
    else: #Error should be thrown, but just in case it isn't
        probtyp = 0
    paths = mtp.getAllPaths()
    boards = []
    for path in paths:
        start = mtp.start
        if( len(path)>100 ):
            print('START NEW PATH (len={}; {})'.format(len(path),f.split('/')[-1]))
        move = None
        outcome = 0
        liveWGr = determineLife(start, False)
        liveBGr = determineLife(start, True)
        w = len(liveWGr)
        b = len(liveBGr)
        boards.append(start)
        print('START: w={}, b={}, nw={}, nb={}'.format(w,b,len(start.white_stones),len(start.black_stones)))
        for mid in path:
            move_dict = mtp.formatMove(mtp.moveID[mid])
            saysblack = move_dict['isBlack'] #move_str[0:1]=='B'
            #print('{}''s turn'.format('black' if saysblack else 'white'))
            move_y = move_dict['y'] #ord(move_str[2]) - ord('a')
            move_x = move_dict['x'] #ord(move_str[3]) - ord('a')
            move = start.clone()
            try:
                move.place_stone(move_x, move_y, saysblack)
                boards.append(move)
                color = 'B' if saysblack else 'W'
                print('{}({},{}): w={}, b={}, nw={}, nb={}'.format(color,move_x,move_y,w,b,len(move.white_stones),len(move.black_stones)))
            except IllegalMove as e:
                print('{}: ({},{})'.format(e, move_x, move_y))
            start = move
        if outcome==1: 
            return move
    return boards

def load_problem_solution(f):
    mtp = MoveTreeParser(f)
    #print('{} := {}'.format(f.split('/')[-1].split('\\')[-1], mtp.problemType))
    sn = mtp.getSolutionNodes()
    inc = mtp.getIncorrectNodes()
    probtyp = mtp.getProblemType()
    if probtyp == 1 or probtyp == 3: #Black to live
        probtyp = 1
    elif probtyp == 2 or probtyp == 4: #White to kill
        probtyp = 2
    else: #Error should be thrown, but just in case it isn't
        probtyp = 0
    isBTL = (probtyp==1) or (probtyp==0) # and mtp.blackFirst)
    if not sn.isdisjoint(inc):
        print('NOT DISJOINT')
    paths = mtp.getAllPaths()
    movesConsidered = set()
    for path in paths:
        parent = 0
        start = mtp.start
        if( len(path)>100 ):
            print('START NEW PATH (len={}; {})'.format(len(path),f.split('/')[-1]))
        move = None
        outcome = 0
        liveWGr = determineLife(start, False)
        liveBGr = determineLife(start, True)
        w = len(liveWGr)
        b = len(liveBGr)
        print('START: w={}, b={}, nw={}, nb={}'.format(w,b,len(start.white_stones),len(start.black_stones)))
        for mid in path:
            move_dict = mtp.formatMove(mtp.moveID[mid])
            saysblack = move_dict['isBlack'] #move_str[0:1]=='B'
            #print('{}''s turn'.format('black' if saysblack else 'white'))
            move_y = move_dict['y'] #ord(move_str[2]) - ord('a')
            move_x = move_dict['x'] #ord(move_str[3]) - ord('a')
            move = start.clone()
            try:
                move.place_stone(move_x, move_y, saysblack)
                color = 'B' if saysblack else 'W'
                print('{}({},{}): w={}, b={}, nw={}, nb={}'.format(color,move_x,move_y,w,b,len(move.white_stones),len(move.black_stones)))
                if (parent, mid) not in movesConsidered:
                    #features = [probtyp]
                    outcome = 0
                    if isBTL == saysblack:
                        #CHECK THIS LOGIC
                        if mid in sn:
                            outcome = 1
                        elif mid in inc:
                            outcome = 0
                        else:
                            raise Exception('Unknown outcome!')
                    else:
                        ''' Assume only moves on incorrect path are correct
                            for the "antagonist" '''
                        if mid in inc:
                            outcome = 1
                        ''' Assume all moves for the "antagonist" are correct '''
                        # outcome = 1
                    movesConsidered.add((parent, mid))
                    #vectors.append(features)
                    # Only train on the first wrong move for the protagonist
                    if outcome==0 and isBTL==saysblack:
                        break;
            except IllegalMove as e:
                print('{}: ({},{})'.format(e, move_x, move_y))
            parent = mid
            start = move
        if outcome==1: 
            return move
    return None

if __name__ == '__main__':
    print("Starting GoLD...")
    if len(sys.argv)>1:
        #solution = load_problem_start(sys.argv[1])
        paths = load_problem_paths(sys.argv[1])
        ui = Launcher(400,400,50,19,board=paths[0])
        ui.showPath(paths)
    else:
        ui = Launcher(400,400,50,19)
        ui.drawBoard()
        ui.mainloop()
