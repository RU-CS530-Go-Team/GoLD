'''
Created on Nov 1, 2014

@author: JBlackmore
'''
from gold.models.board import Board, StoneGrouper, IllegalMove
from gold.learn.trainer import FeatureExtractor
from gold.learn.Model import Model
import numpy as np
from StringIO import StringIO

MAXDEPTH = 2
BEAMSIZE = 2
class MinMaxTree:
    '''
    classdocs
    
    print('Loading model and scaler files...')
    modelFile = 'c:/users/jblackmore/documents/development/rutgers/gold/problems/resplit/trainFeaturesBtl.csv.rf'
    modelType = 3
    model = Model(modelFile, modelType)
    scalerFile = 'c:/users/jblackmore/documents/development/rutgers/gold/problems/resplit/trainFeaturesBtl.csv.scl'
    model.setScaler(scalerFile)
    print('Model and scaler files ready!')
    '''
    def __init__(self, start, isblack, isMinLayer, model=None, depth=0, value=0.0, moveseries=''):
        '''
        Constructor
        '''
        self.board = start
        self.isblack = isblack
        self.isMinLayer = isMinLayer
        self.model = model
        self.depth = depth
        self.children = []
        self.value = value
        self.moveseries = moveseries
        self.remoteSpaces = dict()
        #print("{}={}".format(self.moveseries, self.value))
        self.i = -1
        self.j = -1
        all_stones = self.board.white_stones+self.board.black_stones
        if depth < MAXDEPTH:
            #eggs = []
            validMoves = []
            probs = []
            for i in range(start.x):
                for j in range(start.y):
                    if( (i,j) not in all_stones and self.isNearStones(i,j,isblack)):
                        #move = Board(start.x, start.y)
                        #move.white_stones = [x for x in start.white_stones]
                        #move.black_stones = [y for y in start.black_stones]
                        move = start.clone()
                        try:
                            move.place_stone(i,j,isblack)
                            mval = self.evaluateMove(move,i,j,isblack)
                            #if (not isMinLayer and mval>0) or (isMinLayer and mval<0):
                            if isblack:
                                ms = "{} b({},{})".format(moveseries, i, j)
                            else:
                                ms = "{} w({},{})".format(moveseries, i, j)
                            #mvstr = '%.03f' %mval
                            #print('{} = {}'.format(ms, mvstr))
                            validMoves.append({'board': move, 'prob': mval, 'ms': ms, 'x': i, 'y': j})
                            probs.append(mval)
                            '''
                            child = MinMaxTree(move, not isblack, False, depth+1, self.value+mval, ms)
                            child.i = i
                            child.j = j
                            self.children.append(child)
                            '''
                        except IllegalMove as im:
                            print(im)
            beam = min(len(probs)-1, BEAMSIZE)
            if self.isMinLayer:
                threshold = sorted(probs)[beam]
            else:
                threshold = sorted(probs)[-beam]
            print('Threshold = {}'.format(threshold))
            for vm in validMoves:
                if (vm['prob']<threshold) == self.isMinLayer or vm['prob']==threshold:
                    mvstr = '%.03f' %vm['prob']
                    print('  {} = {}'.format(vm['ms'], mvstr))
                    child = MinMaxTree(vm['board'], not isblack, not isMinLayer, model=model, depth=depth+1, value=vm['prob'], moveseries=vm['ms'])
                    child.i = vm['x']
                    child.j = vm['y']
                    self.children.append(child)

    def evaluateMove(self, move, i, j, isblack):
        fe = FeatureExtractor()
        features = fe.extract_features(self.board, move, (i,j), isblack)
        headers = fe.sort_headers(features.keys())
        #print(headers)
        s1 = ','.join([str(features[header]) for header in headers])+'\n'
        c = StringIO(s1)
        data = np.loadtxt(c,delimiter=',')
        instance = self.model.scale(data)
        prediction = self.model.getScoreCorrect(instance)
        #if self.isMinLayer:
        #    return 1.0-prediction
        return prediction

    def isNearStones(self, i, j, isblack):
        all_stones = self.board.white_stones+self.board.black_stones
        for p in range(5):
            for q in range(5):
                #space = (i+p-2, j+q-2)
                if( (i+p-2, j+q-2) in all_stones ):
                    return True
                #self.remoteSpaces.add((i+p-2,j+q-2))
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
        #self.value = best.value
        #print('best: {}={}'.format(best.moveseries, best.value))
        return best
    
    def decideNextMove(self):
        if self.isMinLayer:
            c = self.bestChild(100000.0)
        else:
            c = self.bestChild(-100000.0)
        '''        
        groups = StoneGrouper(c.board.black_stones).groups
        print('Black has {} groups:'.format(len(groups)))
        for g in groups:
            print('  . {}'.format(g))
        groups = StoneGrouper(c.board.white_stones).groups
        print('White has {} groups:'.format(len(groups)))
        for g in groups:
            print('  . {}'.format(g))
        '''        
        #print('Best move for {}: ({},{})'.format(('black' if self.isblack else 'white'), c.i,c.j))

        return c
