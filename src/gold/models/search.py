'''
Created on Nov 1, 2014

@author: JBlackmore
'''
from gold.models.board import Board

MAXDEPTH = 4
class MinMaxTree:
    '''
    classdocs
    '''
    def __init__(self, start, isblack, isMinLayer, depth, value, moveseries):
        '''
        Constructor
        '''
        self.board = start
        self.isblack = isblack
        self.isMinLayer = isMinLayer
        self.depth = depth
        self.children = []
        self.value = value
        self.moveseries = moveseries
        self.i = -1
        self.j = -1
        all_stones = self.board.white_stones+self.board.black_stones
        if depth < MAXDEPTH:
            bestChild = None
            for i in range(start.x):
                for j in range(start.y):
                    if( (i,j) not in all_stones and self.isNearStones(i,j,isblack)):
                        move = Board(start.x, start.y)
                        move.white_stones = [x for x in start.white_stones]
                        move.black_stones = [y for y in start.black_stones]
                        move.place_stone(i,j,isblack)
                        mval = self.evaluateMove(move,i,j,isblack)
                        if (not isMinLayer and mval>0) or (isMinLayer and mval<0):
                            if isblack:
                                ms = "{} b({},{})".format(moveseries, i, j)
                            else:
                                ms = "{} w({},{})".format(moveseries, i, j)
                            child = MinMaxTree(move, not isblack, not isMinLayer, depth+1, mval, ms)
                            child.i = i
                            child.j = j
                            self.children.append(child)
                            '''
                            if( child.value> self.value and not isMinLayer ):
                                self.value = child.value
                                bestChild = child
                            if( child.value<self.value and isMinLayer ):
                                self.value = child.value
                                bestChild = child
                            '''
                        else:
                            if isblack:
                                print("Rejecting {} black move ({},{}), val={}, depth={}".format(moveseries,i,j,mval,depth))
                            else:
                                print("Rejecting {} white move ({},{}), val={}, depth={}".format(moveseries,i,j,mval, depth))
                            #print("Adding child {} at depth {}: ({},{})".format(len(self.children), depth+1, i, j))
            '''
            if not self.value==value:
                if isblack:
                    print("{} Black should move to ({},{}), val={}, depth={}".format(moveseries, bestChild.i, bestChild.j, bestChild.value, depth))
                else:
                    print("{} White should move to ({},{}), val={}, depth={}".format(moveseries, bestChild.i, bestChild.j, bestChild.value, depth))
            '''
    def evaluateMove(self, move, i, j, isblack):
        blackdiff = len(move.black_stones)-len(self.board.black_stones)
        whitediff = len(move.white_stones)-len(self.board.white_stones)
        print("{}+{}({},{})={}, {}d".format(self.moveseries, ('b' if isblack else 'w'), i,j,blackdiff-whitediff, self.depth))
        return blackdiff - whitediff
    '''
        if isblack:
            return blackdiff - whitediff
        else:
            return whitediff - blackdiff
    '''
    def isNearStones(self, i, j, isblack):
        all_stones = self.board.white_stones+self.board.black_stones
        for p in range(3):
            for q in range(3):
                if( (i+p-1, j+q-1) in all_stones ):
                    '''
                    if( isblack ):
                        print("Adding black child {} at depth {}: ({},{})=>({},{})".format(len(self.children)+1, self.depth+1, i, j, i+p-2,j+q-2))
                    else:
                        print("Adding white child {} at depth {}: ({},{})=>({},{})".format(len(self.children)+1, self.depth+1, i, j, i+p-2,j+q-2))
                    '''
                    return True
        return False
    
    def bestChild(self):
        minmax = 0.0
        best = None
        i=j=-1
        if self.isMinLayer:
            minmax = 100000.0
        for c in self.children:
            b = c.bestChild()
            if b==None:
                b = c
            if b.value < minmax and self.isMinLayer:
                minmax = b.value
                best = c
                i=c.i
                j=c.j
            if b.value > minmax and not self.isMinLayer:
                minmax = b.value
                best = c
                i=c.i
                j=c.j
        if not best==None:
            print('{}={}, {}d-{}d'.format(best.moveseries, best.value, self.depth, best.depth))
        return best
    def decideNextMove(self):
        c = self.bestChild()
        print('Best move for {}: ({},{})'.format(('black' if self.isblack else 'white'), c.i,c.j))
        return [c.i, c.j]
    '''
        minmax = 0.0
        i=j=-1
        if self.isMinLayer:
            minmax = 100000.0
        for c in self.children:
            if c.value < minmax and self.isMinLayer:
                minmax = c.value
                i=c.i
                j=c.j
            if c.value > minmax and not self.isMinLayer:
                minmax = c.value
                i=c.i
                j=c.j
        print("Decided on {}({},{}) with val={}".format(('b' if self.isblack else 'w'),i,j,minmax))
        return [i,j]
        '''