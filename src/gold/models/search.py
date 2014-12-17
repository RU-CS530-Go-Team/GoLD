'''
Created on Nov 1, 2014

@author: JBlackmore
'''
from gold.models.board import IllegalMove
from gold.learn.trainer import FeatureExtractor
from gold.extraneous.life import determineLife
from gold.models.cache import Cache
from gold.features import StoneCountFeature

import time
import numpy as np
from StringIO import StringIO

MAXDEPTH = 3
BEAMSIZE = 10

class MinMaxTree:
    '''
    classdocs
    '''
    maxdepth = MAXDEPTH
    beamsize = BEAMSIZE

    def __init__(self, start, isblack, isMinLayer, blackModel=None, whiteModel=None, level=0, value=None, moveseries='', cache=None):
        '''
        Constructor
        '''
        if cache is None:
            self.cache = Cache()
        else:
            self.cache=cache
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
        self.sb = None
        #print("{}={}".format(self.moveseries, self.value))
        self.i = -1
        self.j = -1


    def node_count(self):
        count=0
        for child in self.children:
            count+=child.node_count()
        return count+1

    def extend_tree(self):
        if self.level >= MinMaxTree.maxdepth:
            return 0
        if self.terminal:
            return 0
        start = time.clock()
        validMoves = self.find_valid_moves()
        nodes_added=0
        hasTerm = False
        bestStoneCount = None
        for vm in validMoves:
            child = MinMaxTree(vm['board'], not self.isblack, not self.isMinLayer,
                               blackModel=self.blackModel, whiteModel=self.whiteModel,
                               level=self.level+1, moveseries=vm['ms'], cache=self.cache)
            child.i = vm['x']
            child.j = vm['y']
            #print('{}'.format(child.moveseries))
            nodes_added+=1
            if vm['term'] is None:
                child.stoneCountDiff = StoneCountFeature(self.board, child.board, child.i, child.j, self.isblack).calculate_feature()[-1]
                if bestStoneCount is None:
                    bestStoneCount = child.stoneCountDiff
                    self.children.append(child)
                elif self.isblack and child.stoneCountDiff>bestStoneCount:
                    bestStoneCount = child.stoneCountDiff
                    self.children = [child]
                elif not self.isblack and child.stoneCountDiff<bestStoneCount:
                    bestStoneCount = child.stoneCountDiff
                    self.children = [child]
                else:
                    self.children.append(child)
                if self.level>0 or len(validMoves)<=MinMaxTree.beamsize:
                    nodes_added+=child.extend_tree()
                    if len(child.children)==1 and child.children[0].terminal and not child.terminal:
                        #print('{}: Propagating terminal case to {}.'.format(child.children[0].moveseries, child.moveseries))
                        child.terminal=True
                        child.value = None
            else:
                child.terminal = True
                if self.isblack:
                    self.children=[child]
                    self.value = self.children[0].value
                    self.terminal = True
                    return 1

        if not self.isblack:
            nonterms = [x for x in self.children if not x.terminal]
            terms = [x for x in self.children if x.terminal]
            # Prune away terminal cases for white
            if len(nonterms)>0 and len(terms)>0:
                print('{}: White evades!'.format(nonterms[0].moveseries))
                self.children = nonterms

        if bestStoneCount is not None:
            if self.isblack:
                self.children = [x for x in self.children if x.stoneCountDiff>=bestStoneCount]
            else:
                self.children = [x for x in self.children if x.stoneCountDiff<=bestStoneCount]

        if self.level==0 and len(validMoves)>MinMaxTree.beamsize:
            self.prune()
            for child in self.children:
                nodes_added+= child.extend_tree()

        return nodes_added

    def terminal_test(self, move, i, j, isblack):
        # Use cache for black-is-alive test
        #black_is_alive = self.cache.get(move)
        black_is_alive=None
        if black_is_alive is None:
            if self.sb is None:
                self.sb =len(determineLife(self.board, True))
            b = len(determineLife(move, True))

            black_is_alive= (b-self.sb)>0
            #self.cache.put(move, black_is_alive)
            result = 2 if black_is_alive else 0
            return [result, b]
        result = 2 if black_is_alive else 0
        return [result, None]

    def find_valid_moves(self):
        all_stones = self.board.white_stones+self.board.black_stones
        validMoves = []
        for i in range(self.board.x):
            for j in range(self.board.y):
                if( (i,j) not in all_stones and self.isNearStones(i,j,self.isblack)):
                    move = self.board.clone()
                    try:
                        move.place_stone(i,j,self.isblack)
                        if self.isblack:
                            ms = "{} b({},{})".format(self.moveseries, i, j)
                        else:
                            ms = "{} w({},{})".format(self.moveseries, i, j)
                        [tt,sb] = self.terminal_test(move, i, j, self.isblack)
                        term_test = self.term_test_to_value(tt, self.isblack)
                        validMove = {'board': move, 'ms': ms, 'x': i, 'y': j, 'term': term_test, 'sb': sb}
                        if term_test is not None and term_test>1.0 and not self.isMinLayer:
                            # This is the solution. Stop and throw away the rest.
                            return [validMove]
                        if term_test is not None and term_test<1.0 and self.isMinLayer:
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
        feats = [0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 19, 20, 21, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243]
        instance = model.setFeatures(instance,feats)
        prediction = model.getScoreCorrect(instance)

        if self.isMinLayer: # and not self.blackModel is self.whiteModel:
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
        if self.children is None or len(self.children)==0:
            return self
        if self.terminal:
            # Coming to life
            if not self.isblack:
                print(self.moveseries+' White has no moves left! Black will live!')
            return self.children[0]
        childrenToEvaluate = []

        for child in self.children:
            if child.terminal:
                if self.isblack:
                    #print ('{} is terminal?'.format(child.moveseries))
                    return child
            else:
                childsBestChild = child.bestChild()
                if childsBestChild is child:
                    # A leaf! Also, non-terminal
                    if self.level==0:
                        childrenToEvaluate.append(child)
                elif childsBestChild.terminal:
                    # White is screwed, its next move will be terminal
                    # Not sure this condition is even possible
                    child.terminal=True
                    child.value=None
                    if self.isblack:
                        return child
                        print('{} Black has white cornered.'.format(child.moveseries))
                else:
                    if self.level==0:
                        childrenToEvaluate.append(child)
        # White's turn, but there's nowhere to go
        if not self.isblack and self.level==0 and len(childrenToEvaluate)==0:
            self.children[0].terminal=True
            return self.children[0]
        best=None
        start = time.clock()
        movesEvaluated = 0
        for child in childrenToEvaluate:
            if child.terminal:
                raise Exception('Internal Error - not expecting terminal cases here.')
            if child.value is None:
                child.value = self.evaluateMove(child.board, child.i, child.j, self.isblack)
                #print('{}: {:.3f}'.format(child.moveseries, child.value))
                movesEvaluated+=1
            if best is None:
                best = child
            if self.isMinLayer and child.value<best.value:
                best = child
            if not self.isMinLayer and child.value>best.value:
                best = child
        #if movesEvaluated>0:
            #print('Evaluated {} valid moves in {:.1f} seconds.'.format(movesEvaluated, time.clock()-start))

        if best is None:
            if len(self.children)>0:
                return self.children[0]
            return self
        return best


    def promote(self, newlevel=0, extendIfSame=False):
        ''' Changes level of node to higher in the tree.
            Default level is 0, making self the new root.
            If newlevel is less than current level, recursively
            extends tree to MAXDEPTH
        '''
        if newlevel>self.level:
            raise ValueError('Cannot increase level when promoting ({}>{})'.format(newlevel>self.level))
        if newlevel==self.level and not extendIfSame:
            return 0
        self.level=newlevel
        start = time.clock()
        nodes_added=0
        if self.children is None or len(self.children)==0:
            nodes_added+=self.extend_tree()
        else:
            if self.level==0:
                self.prune()
            for child in self.children:
                nodes_added+=child.promote(newlevel+1)
            #if self.level==0:
            #    print('Promotion added {} nodes in {:.1f} seconds'.format(nodes_added, time.clock()-start))
                #print('There are now {} nodes total.'.format(self.node_count()))
        return nodes_added

    def prune(self, stone=None):
        if stone is not None:
            newChildren = []
            [x,y]=stone
            for child in self.children:
                if child.i!=x or child.j!=y:
                    newChildren.append(child)
                else:
                    print('Pruned illegal move ({},{})'.format(x,y))
            self.children = newChildren
        if len(self.children)>MinMaxTree.beamsize:
            # Evaluate all moves, choose top k to search to depth d for terminal states
            for child in self.children:
                child.value = self.evaluateMove(child.board, child.i, child.j, self.isblack)
            # Search the most likely moves in the proper order
            cutoff = min(MinMaxTree.beamsize, len(self.children)-1)
            self.children= sorted(self.children, key=lambda child: child.value, reverse=(not self.isMinLayer))[:cutoff]

    def decideNextMove(self):
        c = self.bestChild()
        if c is self:
            return None
        return c
#class BeamMMTree(MinMaxTree):
