'''
Created on Nov 1, 2014

@author: JBlackmore
'''
from gold.models.board import Board, StoneGrouper, IllegalMove
from gold.learn.trainer import FeatureExtractor
from gold.learn.Model import Model
import numpy as np
from StringIO import StringIO

MAXDEPTH = 1
BEAMSIZE = 3
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
    def __init__(self, start, isblack, isMinLayer, blackModel=None, whiteModel=None, level=0, value=0.0, moveseries=''):
        '''
        Constructor
        '''
        self.board = start
        self.isblack = isblack
        self.isMinLayer = isMinLayer
        self.blackModel = blackModel
        self.whiteModel = whiteModel
        self.level = level
        self.children = []
        self.value = value
        self.moveseries = moveseries
        self.remoteSpaces = dict()
        #print("{}={}".format(self.moveseries, self.value))
        self.i = -1
        self.j = -1
        if level < MAXDEPTH:
            #eggs = []
            self.extend_tree()


    def extend_tree(self):
        validMoves = self.find_valid_moves()
        probs = [x['prob'] for x in validMoves]
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
                child = MinMaxTree(vm['board'], not self.isblack, not self.isMinLayer, blackModel=self.blackModel, whiteModel=self.whiteModel, level=self.level+1, value=vm['prob'], moveseries=vm['ms'])
                child.i = vm['x']
                child.j = vm['y']
                self.children.append(child)

    def find_valid_moves(self):
        all_stones = self.board.white_stones+self.board.black_stones
        validMoves = []
        for i in range(self.board.x):
            for j in range(self.board.y):
                if( (i,j) not in all_stones and self.isNearStones(i,j,self.isblack)):
                    move = self.board.clone()
                    try:
                        move.place_stone(i,j,self.isblack)
                        mval = self.evaluateMove(move,i,j,self.isblack)
                        if self.isblack:
                            ms = "{} b({},{})".format(self.moveseries, i, j)
                        else:
                            ms = "{} w({},{})".format(self.moveseries, i, j)
                        #mvstr = '%.03f' %mval
                        #print('{} = {}'.format(ms, mvstr))
                        validMoves.append({'board': move, 'prob': mval, 'ms': ms, 'x': i, 'y': j})
                    except IllegalMove as im:
                        print(im)
        return validMoves

    def evaluateMove(self, move, i, j, isblack):
        fe = FeatureExtractor()
        features = fe.extract_features(self.board, move, (i,j), isblack)
        headers = fe.sort_headers(features.keys())
        #print(headers)
        s1 = ','.join([str(features[header]) for header in headers])+'\n'
        c = StringIO(s1)
        data = np.loadtxt(c,delimiter=',')
        if isblack:
            model = self.blackModel
        else:
            model = self.whiteModel
        instance = model.scale(data)
        prediction = model.getScoreCorrect(instance)

        if self.isMinLayer:
            return prediction
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


    def bestChild(self):
        minmax = -100000.0
        best = self
        if self.isMinLayer:
            minmax = 100000.0
        for c in self.children:
            b = c.bestChild()
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
        #print('best: {}={}'.format(best.moveseries, best.value))
        return best


    def promote(self, newlevel=0):
        ''' Changes level of node to higher in the tree.
            Default level is 0, making self the new root.
            If newlevel is less than current level, recursively
            extends tree to MAXDEPTH
        '''
        if newlevel>self.level:
            raise ValueError('Cannot increase level when promoting ({}>{})'.format(newlevel>self.level))
        if newlevel==self.level:
            return
        if self.children==None or len(self.children)==0:
            self.extend_tree()
        else:
            for child in self.children:
                child.promote(newlevel+1)
        return self

    def decideNextMove(self):
        c = self.bestChild()
        return c
