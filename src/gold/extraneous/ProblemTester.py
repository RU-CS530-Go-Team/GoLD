'''
Created on Nov 28, 2014

@author: JBlackmore
'''
from gold.extraneous.MoveTreeParser import MoveTreeParser
from gold.models.board import Board
import sys
from gold.learn.trainer import FeatureExtractor
from gold.models.search import MinMaxTree
from gold.ui.Launcher import Launcher
from gold.extraneous.life import determineLife

def print_move(label, move):
    liveWGr = determineLife(move, False)
    liveBGr = determineLife(move, True)
    w = len(liveWGr)
    b = len(liveBGr)
    print('{}: w={}, b={}, nw={}, nb={}'.format(label,w,b,len(move.white_stones),len(move.black_stones)))
    
def test_problem(probfile):
    mtp = MoveTreeParser(probfile)
    print('BF={}'.format(mtp.blackFirst))
    print('Typ={} {}'.format(mtp.getProblemTypeDesc(), '(flipped)' if mtp.isColorFlipped() else ''))
    ss = mtp.getSolutionPaths()
    fe = FeatureExtractor()
    isblack = mtp.blackFirst != mtp.flipColors
    move = mtp.start.clone()
    solutionStates = set()
    print_move('start ({}x{})'.format(move.x, move.y), move)
    
    for spath in ss:
        move = mtp.start.clone()
        #w = len(determineLife(move, False))
        #b = len(determineLife(move, True))
        for step in spath:
            fm = mtp.formatMove(mtp.moveID[step])
            move.place_stone(fm['x'], fm['y'], fm['isBlack'])
            w = len(determineLife(move, False))
            b = len(determineLife(move, True))
            color = 'B' if fm['isBlack'] else 'W'
            if step in mtp.solutionStates:
                solutionStates.add((w,b))
            print_move('{}({},{})'.format(color,fm['x'],fm['y']), move)
            #print('{}({},{}): w={}, b={}, nw={}, nb={}'.format(color, fm['x'],fm['y'],w,b,len(move.white_stones),len(move.black_stones)))
            #print('({},{})={}'.format(fm['x'],fm['y'],fe.extract_features(start, move, (fm['x'], fm['y']), fm['isBlack'])))
        print('------------')

    w = len(determineLife(mtp.start, False))
    b = len(determineLife(mtp.start, True))
    #color = 'B' if isblack else 'W'
    #print('start: w={}, b={},nw={},nb={} {}x{}'.format(w,b, len(mtp.start.white_stones),len(mtp.start.black_stones),move.x, move.y))
    
    move = mtp.start.clone()
    while( (w,b) not in solutionStates ):
        color = 'B' if isblack else 'W'
        mmt = MinMaxTree(move, isblack, not isblack, 0, 0.0, '')
        nextMove = mmt.decideNextMove()
        #priorStates.append([[x for x in move.white_stones], [y for y in move.black_stones]])
        #beforeMove = move.clone()
        move.place_stone(nextMove.i, nextMove.j, isblack)
        w = len(determineLife(move,False))
        b = len(determineLife(move, True))
        print('{}({},{}): w={}, b={}, nw={}, nb={}'.format(color, nextMove.i, nextMove.j,w,b,len(move.white_stones),len(move.black_stones)))
        isblack = not isblack
    print('Problem SOLVED')
    '''
    ui=Launcher(400,400,50,max(move.x,move.y))
    ui.setBoard(move)
    ui.drawBoard()
    ui.mainloop()
    '''
    
def been_here_before(priorStates, currentState):
    for prior in priorStates:
        whiteSet = prior[0]
        blackSet = prior[1]
        cwset = currentState[0]
        cbset = currentState[1]
        if whiteSet == cwset and blackSet==cbset:
            print('W1: {}'.format(whiteSet))
            print('W2: {}'.format(cwset))
            print('B1: {}'.format(blackSet))
            print('B2: {}'.format(cbset))
            return True
    return False

if __name__ == '__main__':
    #test_problem(sys.argv[1])
    test_problem('C:/Users/jblackmore/Documents/Development/Rutgers/GoLD/problems/resplit/train/25k/4131.sgf')
    #test_problem('C:/Users/jblackmore/Documents/Development/Rutgers/GoLD/problems/resplit/train/25k/3052.sgf')
    test_problem('C:/Users/jblackmore/Documents/Development/Rutgers/GoLD/problems/resplit/train/25k/8177.sgf')
    