'''
Created on Nov 1, 2014

@author: JBlackmore
'''
from gold.models.board import IllegalMove
from gold.learn.trainer import FeatureExtractor
from gold.extraneous.life import determineLife
from gold.models.cache import Cache

import time
import numpy as np
from StringIO import StringIO

MAXDEPTH = 3
BEAMSIZE = 50

 
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
        if self.level==0:
            print('Found {} valid moves.'.format(len(validMoves)))
        nodes_added=0
        hasTerm = False
        for vm in validMoves:
            child = MinMaxTree(vm['board'], not self.isblack, not self.isMinLayer, 
                               blackModel=self.blackModel, whiteModel=self.whiteModel, 
                               level=self.level+1, moveseries=vm['ms'], cache=self.cache)
            child.i = vm['x']
            child.j = vm['y']
            #print('{}'.format(child.moveseries))
            nodes_added+=1
            if vm['term'] is None:
                self.children.append(child)
                if hasTerm and not self.isblack:
                    print('{} White can escape.'.format(child.moveseries))
                if self.level>0:
                    nodes_added+=child.extend_tree()
                    if len(child.children)==1 and child.children[0].terminal and not child.terminal:
                        #print('{}: Propagating terminal case to {}.'.format(child.children[0].moveseries, child.moveseries))
                        child.terminal=True
                        child.value = None
                        #child.value = child.children[0].value
            else:
                child.terminal = True
                if self.isblack:
                    self.children=[child]
                    return 1

        if not self.isblack:
            nonterms = [x for x in self.children if not x.terminal]
            terms = [x for x in self.children if x.terminal]
            if len(nonterms)>0 and len(terms)>0:
                print('{}: White evades!'.format(nonterms[0].moveseries))
                self.children = nonterms
        # White is screwed. No non-terminal moves left. 
        
        if not self.isblack and len(self.children)==0 and len(validMoves)>0:
            vm = validMoves[0]
            print('{} White is screwed.'.format(self.moveseries))
            self.children=[MinMaxTree(vm['board'], not self.isblack, not self.isMinLayer, 
                               blackModel=self.blackModel, whiteModel=self.whiteModel, 
                               level=self.level+1, moveseries=vm['ms'], cache=self.cache)]
        if len(self.children)==1 and self.children[0].terminal:
            print('{}: Assigning terminal value to myself because my only child is terminal'.format(self.children[0].moveseries))
            self.value = self.children[0].value
            self.terminal = True
            
        # Evaluate all first moves
        if self.level==0:
            print('Created {} children in {:.1f} seconds.'.format(len(self.children), time.clock()-start))
            start = time.clock()
            print('Evaluating {} moves'.format(len(self.children)))
            beam = min(MinMaxTree.beamsize, len(self.children))
            if beam<=len(self.children):
                children = self.children
            else:
                for child in self.children:
                    child.value = self.evaluateMove(child.board, child.i, child.j, self.isblack)
                    print('{}: {}'.format(child.moveseries, child.value))
                children= sorted(self.children, key=lambda child: child.value, reverse=(not self.isMinLayer))[:min(MinMaxTree.beamsize, len(self.children)-1)]
                # Search the most likely moves in the proper order
                print('Evaluated {} moves in {:.1f} seconds.'.format(len(self.children), start))

            start = time.clock()
            for child in children:
                #cstart=time.clock()
                nodes_added+= child.extend_tree()
                #print('  {}: {:.1f} sec.'.format(nodes_added, time.clock()-cstart))
            print('Extended tree by {} nodes in {:.1f} seconds.'.format(nodes_added, time.clock()-start))
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
                        #mval = self.evaluateMove(move,i,j,self.isblack)
                        if self.isblack:
                            ms = "{} b({},{})".format(self.moveseries, i, j)
                        else:
                            ms = "{} w({},{})".format(self.moveseries, i, j)
                        #mvstr = '%.03f' %mval
                        #print('{} = {}'.format(ms, mvstr))
                        #self.terminal_test(move, i, j, self.isblack)
                        [tt,sb] = self.terminal_test(move, i, j, self.isblack)
                        term_test = self.term_test_to_value(tt, self.isblack)
                        validMove = {'board': move, 'ms': ms, 'x': i, 'y': j, 'term': term_test, 'sb': sb}
                        if term_test is not None and term_test>1.0 and not self.isMinLayer:
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
        if self.children is None or len(self.children)==0:
            return self
        if self.terminal:
            # Already dead
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
        if not self.isblack and self.level==0 and len(childrenToEvaluate)==0 and len(self.children)>0:
            self.children[0].terminal=True
            return self.children[0]
        best=None
        for child in childrenToEvaluate:
            if child.terminal:
                raise Exception('Internal Error - not expecting terminal cases here.')
            if child.value is None:
                child.value = self.evaluateMove(child.board, child.i, child.j, self.isblack)
            if best is None:
                best = child
            if self.isMinLayer and child.value<best.value:
                best = child
            if not self.isMinLayer and child.value>best.value:
                best = child
        if best is None:
            if len(self.children)>0:
                return self.children[0]
            return self
        return best


    def bestChildOld(self):
        minmax = -100000.0
        best = self
        if self.isMinLayer:
            minmax = 100000.0
        childrenToEvaluate = []
        for c in self.children:
            b = c.bestChild()
            c.value = b.value
        
            if b is None:
                raise Exception('Unexpected error - child not found.')
            # b should either be a child which is a leaf or the child's best child
            
            if (b.value is None or not b.terminal):
                # Evaluate leaves first
                childrenToEvaluate.append(b)
            # probably means it's terminal
            if b.value is None:
                #if c.level>2:
                #    print('{}: Found a non-terminal case.'.format(b.moveseries))
                if self.isMinLayer: 
                    #if minmax==2.0:
                    
                    #    print(b.moveseries+': Unevaluated move is likely better than this:')
                    #    print(best.moveseries+': See?')
                    if best.value is not None:
                        #print(c.moveseries+': Avoided unconditional life')
                        best = c
            else:
                #if not b.terminal:
                #    print('Weird, value but not terminal')
                    
                #if self.isMinLayer and b.terminal:
                #   print('{}: MM={}. Found a terminal case w/ c.v=None. Now what? I don''t want it.'.format(b.moveseries, b.value))
                #elif not self.isMinLayer:
                #print('{}: MM={}. Found a terminal case.'.format(b.moveseries, b.value))
                if self.isMinLayer and (c.value is not None and c.value < minmax) or c.value is None:
                    minmax = c.value
                    best = c
                    #if minmax>1.0 or minmax<0:
                    #    print('{}: MM={}. Found a terminal case. Now what? I don''t want it.'.format(c.moveseries, minmax))
                        
                elif c.value is not None and c.value > minmax and not self.isMinLayer:
                    minmax = c.value
                    best = c
                    if minmax>1.0:
                        self.value = best.value
                        return best
        
        #if self.isMinLayer and best.value is not None:
        #    print('{}: White=screwed.'.format(best.moveseries))
        #self.value = best.value
        # Only compute probability for children at next level
        if self.level==0: # or (self.isMinLayer and minmax>1):
            # No terminal test cases, now evaluate the rest
            #for i in range(min(MinMaxTree.beamsize, len(childrenToEvaluate))):
            for c in childrenToEvaluate:
                #c = childrenToEvaluate[i]
                if c.value is None:
                    c.value = self.evaluateMove(c.board, c.i, c.j, self.isblack)
                    
                if self.isMinLayer and c.value < minmax:
                    minmax = c.value
                    best = c
                elif c.value > minmax and not self.isMinLayer:
                    minmax = c.value
                    best = c
            self.value = best.value
            #print('Search took {:.1f} seconds ({} nodes, depth={}).'.format(time.clock()-start, len(self.children), MinMaxTree.maxdepth))
        #print('best: {}={}'.format(best.moveseries, best.value))
        #if self.level==0:
        #    for c in self.children:
        #        print('{}: VAL={}.'.format(c.moveseries, c.value))
        #    print('{}: VAL={}.'.format(best.moveseries, best.value))
            
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
            return 0
        self.level=newlevel
        start = time.clock()
        nodes_added=0
        if self.children is None or len(self.children)==0:
            nodes_added+=self.extend_tree()
        else:
            for child in self.children:
                nodes_added+=child.promote(newlevel+1)
            #if self.level==0:
            #    print('Promotion added {} nodes in {:.1f} seconds'.format(nodes_added, time.clock()-start))
                #print('There are now {} nodes total.'.format(self.node_count()))
        return nodes_added

    def decideNextMove(self):
        c = self.bestChild()
        if c is self:
            return None
        return c
