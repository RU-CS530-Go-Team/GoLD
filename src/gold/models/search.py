'''
Created on Nov 1, 2014

@author: JBlackmore
'''
from gold.models.board import Board, StoneGrouper
from gold.features.StoneCountFeature import StoneCountFeature

MAXDEPTH = 3
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
        #print("{}={}".format(self.moveseries, self.value))
        self.i = -1
        self.j = -1
        all_stones = self.board.white_stones+self.board.black_stones
        if depth < MAXDEPTH:
            for i in range(start.x):
                for j in range(start.y):
                    if( (i,j) not in all_stones and self.isNearStones(i,j,isblack)):
                        move = Board(start.x, start.y)
                        move.white_stones = [x for x in start.white_stones]
                        move.black_stones = [y for y in start.black_stones]
                        move.place_stone(i,j,isblack)
                        mval = self.evaluateMove(move,i,j,isblack)
                        #if (not isMinLayer and mval>0) or (isMinLayer and mval<0):
                        if isblack:
                            ms = "{} b({},{})".format(moveseries, i, j)
                        else:
                            ms = "{} w({},{})".format(moveseries, i, j)
                        child = MinMaxTree(move, not isblack, not isMinLayer, depth+1, self.value+mval, ms)
                        child.i = i
                        child.j = j
                        self.children.append(child)
            
    def evaluateMove(self, move, i, j, isblack):
        features = [StoneCountFeature(self.board, move, (i,j), isblack).calculate_feature()]
        # h(x) = scikit-learn...
        return features[0]

    def isNearStones(self, i, j, isblack):
        all_stones = self.board.white_stones+self.board.black_stones
        for p in range(5):
            for q in range(5):
                if( (i+p-2, j+q-2) in all_stones ):
                    return True
        return False


    def bestChild(self, pruneValue):
        minmax = -100000.0
        best = self
        if self.isMinLayer:
            minmax = 100000.0
        for c in self.children:
            b = c.bestChild(minmax)
            if not b==None:
                #print('{}={}+({},{})={} => {}'.format(c.moveseries, c.value, b.i,b.j,b.value,b.value+c.value))
                c.value = b.value
                if self.isMinLayer and c.value < minmax:
                    minmax = c.value
                    best = c
                elif c.value > minmax and not self.isMinLayer:
                    minmax = c.value
                    best = c
        self.value = best.value
        return best
    
    def decideNextMove(self):
        if self.isMinLayer:
            c = self.bestChild(100000.0)
        else:
            c = self.bestChild(-100000.0)
        print('Best move for {}: ({},{})'.format(('black' if self.isblack else 'white'), c.i,c.j))
        groups = StoneGrouper(c.board.black_stones).groups
        print('Black has {} groups:'.format(len(groups)))
        for g in groups:
            print('  . {}'.format(g))
        groups = StoneGrouper(c.board.white_stones).groups
        print('White has {} groups:'.format(len(groups)))
        for g in groups:
            print('  . {}'.format(g))
        return [c.i, c.j]
