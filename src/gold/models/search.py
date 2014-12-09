'''
Created on Nov 1, 2014

@author: JBlackmore
'''
from gold.models.board import Board, StoneGrouper, IllegalMove
from gold.learn.trainer import FeatureExtractor
from gold.learn.Model import Model
from gold.extraneous.life import determineLife

import time
import numpy as np
from StringIO import StringIO

MAXDEPTH = 3
BEAMSIZE = 1

    
class MinMaxTree:
    '''
    classdocs
    '''
    maxdepth = MAXDEPTH
    
    def __init__(self, start, isblack, isMinLayer, blackModel=None, whiteModel=None, level=0, value=None, moveseries=''):
        '''
        Constructor
        '''
        self.terminal=False
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
        if level < MinMaxTree.maxdepth-1 and not self.terminal:
            #eggs = []
            self.extend_tree()


    def extend_tree(self):
        if self.terminal:
        #if self.value is not None and (self.value==2.0 or self.value<0.0):
            #print('{}: Cutting off search B, terminal state found'.format(self.moveseries, self.value))
            return self
        start = time.clock()
        validMoves = self.find_valid_moves()
        #if self.level==0:
        #    print("Finding valid moves for {} to depth={}".format('black' if self.isblack else 'white', MinMaxTree.maxdepth))
        ##probs = [x['prob'] for x in validMoves]
        #beam = min(len(probs)-1, BEAMSIZE)

        for vm in validMoves:
            child = MinMaxTree(vm['board'], not self.isblack, not self.isMinLayer, 
                               blackModel=self.blackModel, whiteModel=self.whiteModel, 
                               level=self.level+1, value=vm['term'], moveseries=vm['ms'])
            if vm['term'] is not None:
                #print('{} is TERMINAL'.format(child.moveseries))
                child.terminal = True
                #if not self.isblack and self.level==0:
                #    print(' T:{}'.format(vm['ms']))
            child.i = vm['x']
            child.j = vm['y']
            self.children.append(child)
        #if self.level==0:
        #    print("Tree with {} initial moves expanded to depth={} constructed in {:.1f} seconds.".format(len(validMoves), MinMaxTree.maxdepth, time.clock()-start))        
        '''
        if self.isMinLayer:
            threshold = sorted(probs)[beam]
        else:
            threshold = sorted(probs)[-beam]
        '''
        #print('Threshold = {}'.format(threshold))
        '''
        for vm in validMoves:
            if (vm['prob']<threshold) == self.isMinLayer or vm['prob']==threshold:
                mvstr = '%.03f' %vm['prob']
                #print('  {} = {}'.format(vm['ms'], mvstr))
                #child = MinMaxTree(vm['board'], not self.isblack, not self.isMinLayer, blackModel=self.blackModel, whiteModel=self.whiteModel, level=self.level+1, value=vm['prob'], moveseries=vm['ms'])
            child = MinMaxTree(vm['board'], not self.isblack, not self.isMinLayer, blackModel=self.blackModel, whiteModel=self.whiteModel, level=self.level+1, moveseries=vm['ms'])
            child.i = vm['x']
            child.j = vm['y']
            self.children.append(child)
        '''
        return self
    
    def terminal_test(self, move, i, j, isblack):
        sb = len(determineLife(self.board, True))
        b = len(determineLife(move, True))
        #if self.isblack:
        #    ms = "{} b({},{})".format(self.moveseries, i, j)
        #else:
        #    ms = "{} w({},{})".format(self.moveseries, i, j)
        if (b-sb)>0:
            # black lives
            #print('{}: Black lives!'.format(ms))
            return 2
        return 0
    
    def find_valid_moves(self):
        all_stones = self.board.white_stones+self.board.black_stones
        validMoves = []
        for i in range(self.board.x):
            for j in range(self.board.y):
                if( (i,j) not in all_stones and self.isNearStones(i,j,self.isblack)):
                    move = self.board.clone()
                    try:
                        move.place_stone(i,j,self.isblack)
                        #mval = self.evaluateMove(move,i,j,self.isblack)
                        if self.isblack:
                            ms = "{} b({},{})".format(self.moveseries, i, j)
                        else:
                            ms = "{} w({},{})".format(self.moveseries, i, j)
                        #mvstr = '%.03f' %mval
                        #print('{} = {}'.format(ms, mvstr))
                        #self.terminal_test(move, i, j, self.isblack)
                        term_test = self.term_test_to_value(self.terminal_test(move, i, j, self.isblack), self.isblack)
                        validMove = {'board': move, 'ms': ms, 'x': i, 'y': j, 'term': term_test}
                        if term_test>1.0 and not self.isMinLayer:
                            # This is the solution. Stop and throw away the rest. 
                            #print('{}: Cutting off search A, terminal state found'.format(ms, self.value))
                            return [validMove]
                        if term_test is not None and term_test<1.0 and self.isMinLayer:
                            #print('{}: Cutting off search C, terminal state found'.format(ms, self.value))
                            return [validMove]
                        validMoves.append(validMove)
                    except IllegalMove:
                        pass
        return validMoves

    def term_test_to_value(self, term_test, isblack):
        if term_test==2:
            # Black lives
            if isblack:
                if self.isMinLayer:
                    return -1
                return 2
            else:
                if self.isMinLayer:
                    return 2
                return -1
        if term_test==-1:
            # White kills
            if isblack:
                if self.isMinLayer:
                    return 2
                return -1
            else:
                if self.isMinLayer:
                    return -1
                return 2
        return None
    
    def evaluateMove(self, move, i, j, isblack):
        #term_test = self.term_test_to_value(self.terminal_test(move, i, j, isblack), isblack)
        #if term_test is not None:
        #    return term_test
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
            return 1.0-prediction
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
        start = time.clock()
        best = self
        #if self.level==0:
        #    print('Searching for best move ({} nodes, depth={}).'.format(len(self.children), MinMaxTree.maxdepth))
        if self.isMinLayer:
            minmax = 100000.0
        childrenToEvaluate = []
        for c in self.children:
            b = c.bestChild()
            if b is None:
                raise Exception('Unexpected error - child not found.')
            if b is c and (b.value is None or not b.terminal):
                # Evaluate leaves first
                childrenToEvaluate.append(b)
            if b.value is not None:
                c.value = b.value
                if self.isMinLayer and c.value < minmax:
                    minmax = c.value
                    best = c
                elif c.value > minmax and not self.isMinLayer:
                    minmax = c.value
                    best = c
                    if minmax>1.0:
                        self.value = best.value
                        return best
        
        self.value = best.value
        # Only compute probability for children at next level
        if self.level==0:
            # No terminal test cases, now evaluate the rest
            for c in childrenToEvaluate:
                if c.value is None:
                    c.value = self.evaluateMove(c.board, c.i, c.j, self.isblack)
                if self.isMinLayer and c.value < minmax:
                    minmax = c.value
                    best = c
                elif c.value > minmax and not self.isMinLayer:
                    minmax = c.value
                    best = c
            #print('Search took {:.1f} seconds ({} nodes, depth={}).'.format(time.clock()-start, len(self.children), MinMaxTree.maxdepth))
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
        self.level=newlevel
        if self.children==None or len(self.children)==0:
            self.extend_tree()
        else:
            for child in self.children:
                child.promote(newlevel+1)
        return self

    def decideNextMove(self):
        c = self.bestChild()
        if c==self:
            return None
        return c
