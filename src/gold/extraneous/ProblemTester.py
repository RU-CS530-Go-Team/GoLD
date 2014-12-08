'''
Created on Nov 28, 2014

@author: JBlackmore
'''
from gold.extraneous.MoveTreeParser import MoveTreeParser,\
    UnspecifiedProblemType
from gold.models.board import Board, IllegalMove
from random import seed, shuffle
import csv
import sys
import os
from gold.learn.trainer import FeatureExtractor
from gold.models.search import MinMaxTree
from gold.ui.Launcher import Launcher
from gold.extraneous.life import determineLife
from gold.extraneous.terminalLife import findAliveGroups
from gold.learn.Model import Model
from glob import glob

def print_move(label, move):
    liveWGr = determineLife(move, False)
    liveBGr = determineLife(move, True)
    w = len(liveWGr)
    b = len(liveBGr)
    #aliveWGr = findAliveGroups(move, False)
    #aliveBGr = findAliveGroups(move, True)
    wa = 0#len(aliveWGr)
    wb = 0#len(aliveBGr)
    print('{}: w={}, b={}, wa={}, wb={}, nw={}, nb={}'.format(label,w,b,wa,wb,len(move.white_stones),len(move.black_stones)))

''' Checks problem type and number of living groups
    against terminal states from the problem. 
'''
def term_test(probfile, testResults=dict()):
    mtp = MoveTreeParser(probfile)
    ss = mtp.getAllPaths()
    move = mtp.start.clone()
    #print_move('start ({}x{})'.format(move.x, move.y), move)
    isBtL = (mtp.problemType == 1 or mtp.problemType==3)
    pt = 1 if isBtL else 2
    testResults['PT'] = pt
    sw = len(determineLife(move, False))
    sb = len(determineLife(move, True))
    if sb>0:
        print('{}: Black is already alive!'.format(probfile))
    # prob type, solution, terminal, # living black groups, # living white groups
    #tpl= (pt, 1, 0, sb, sw)
    tpl= (pt, 1, 0, 0, 0)
    if tpl in testResults.keys():
        testResults[tpl] = testResults[tpl]+1
    else:
        testResults[tpl]=1
    for spath in ss:
        move = mtp.start.clone()
        for step in spath:
            fm = mtp.formatMove(mtp.moveID[step])
            move.place_stone(fm['x'], fm['y'], fm['isBlack'])
            w = len(determineLife(move, False))
            b = len(determineLife(move, True))
            sol = 1 if step in mtp.getSolutionNodes() else 0
            term = 1 if step in mtp.getTerminalStates() else 0
            bdiff = b-sb
            wdiff = w-sw    
            tpl = (pt, sol, term, b, w)
            if tpl in testResults.keys():
                testResults[tpl] = testResults[tpl]+1
            else:
                testResults[tpl]=1
    return testResults

def test_problem(probfile, modelBtL, modelWtK):
    print(probfile)
    mtp = MoveTreeParser(probfile)
    ss = mtp.getSolutionPaths()
    isblack = mtp.blackFirst != mtp.flipColors
    move = mtp.start.clone()
    solutionStates = set()
    terminalIncorrectStates = set()
    print_move('start ({}x{})'.format(move.x, move.y), move)
    longestPath = 0
    isBtL = (mtp.problemType == 1 or mtp.problemType==3)
    print(mtp.getProblemTypeDesc()+' - black={}, isBtL={}'.format(isblack, isBtL))
    for spath in ss:
        pathLength = 0
        move = mtp.start.clone()
        #w = len(determineLife(move, False))
        #b = len(determineLife(move, True))
        for step in spath:
            pathLength += 1
            if pathLength>longestPath:
                longestPath = pathLength
            fm = mtp.formatMove(mtp.moveID[step])
            move.place_stone(fm['x'], fm['y'], fm['isBlack'])
            color = 'B' if fm['isBlack'] else 'W'
            print_move('{}({},{})'.format(color,fm['x'],fm['y']), move)
            if step in mtp.getTerminalStates():
                if step in mtp.getSolutionStates():
                    solutionStates.add(move.clone())
                else:
                    terminalIncorrectStates.add(move.clone())

        print('------------')

    move = mtp.start.clone()
    #b = len(determineLife(move,True))
    pathLength = 0
    if isblack:
        mmt = MinMaxTree(move, True, not isBtL, blackModel=modelBtL, whiteModel=modelWtK)
    else:
        mmt = MinMaxTree(move, False, isBtL, blackModel=modelBtL, whiteModel=modelWtK)
    while( move not in solutionStates and pathLength<2*longestPath):
        color = 'B' if isblack else 'W'
        mmt = mmt.decideNextMove()
        move.place_stone(mmt.i, mmt.j, isblack)
        #b = len(determineLife(move,True))
        print_move('{}({},{})'.format(color,mmt.i, mmt.j), move)
        mmt.promote()
        if move in terminalIncorrectStates:
            raise 'Haha! You lose!'
        if move in solutionStates:
            print('{}: You Win!!'.format(probfile))
            return
        pathLength = pathLength+1
        #w = len(deter(move,False))
        #b = len(findAliveGroups(move, True))
        #print('{}({},{}): w={}, b={}, nw={}, nb={}'.format(color, nextMove.i, nextMove.j,w,b,len(move.white_stones),len(move.black_stones)))
        isblack = not isblack
    raise Exception('Too many moves, you lose!!')
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

def load_model(modelFile, modelType, scalerFile):
    print('Loading model and scaler files...')
    model = Model(modelFile, modelType)
    model.setScaler(scalerFile)
    print('Model and scaler files ready!')
    return model
if __name__ == '__main__':
    if len(sys.argv)<3:
        print('Usage: python ProblemTester <model_dir> <problem_dir>')
        sys.exit()
    modelDir = sys.argv[1]
    problemDirs = sys.argv[2:]
    print(problemDirs)
    modelFile = modelDir+'/modelRF100BtL.txt'
    modelType = 3 
    scalerFile = modelDir+'/trainfeaturesBtLScaler.txt'
    modelBtL = load_model(modelFile, modelType, scalerFile)
    modelFile = modelDir+'/modelRF100WtK.txt'
    modelType = 3
    scalerFile = modelDir+'/trainfeaturesWtKScaler.txt'
    modelWtK = load_model(modelFile, modelType, scalerFile)
    #test_problem(sys.argv[1], modelBtL, modelWtK)

    terms = dict()
    seed(1234567890)
    totalNumCorrect = 0
    totalTotal = 0
    for problemDir in problemDirs:
        numCorrect = 0
        numTotal = 0
        if not os.path.isdir(problemDir):
            if len(problemDir)<3:
                print('Not a dir or problem file: {}'.format(problemDir))
            elif problemDir[-3]=='sgf':
                test_problem(problemDir, modelBtL, modelWtK)
                #terms = term_test(problemDir, terms)
            else:
                print('Not a dir or problem file: {}'.format(problemDir))
            sys.exit()
        dirs = glob(problemDir+'/*')
        shuffle(dirs)
        for probdiff in dirs:
            if os.path.isdir(probdiff):
                files = glob(probdiff+'/*.sgf')
                for probfile in files:
                    
                    print(probfile)
                    try:
                        #terms = term_test(probfile, terms)
                        test_problem(probfile, modelBtL, modelWtK)
                        numCorrect += 1
                        numTotal += 1
                    except UnspecifiedProblemType:
                        x= 'UPT'
                    except IllegalMove as im:
                        print(im)
                    except Exception as e:
                        numTotal += 1
                        print(e)
            else:
                if probdiff[-3:]=='sgf':
                    try:
                        #terms = term_test(probfile, terms)
                        test_problem(probdiff, modelBtL, modelWtK)
                        numCorrect += 1
                        numTotal += 1
                    except UnspecifiedProblemType:
                        x= 'UPT'
                    except IllegalMove as im:
                        print(im)
                    except Exception as e:
                        print(e)
                        x = 'WHATEVER'
        totalNumCorrect+=numCorrect
        totalTotal+=numTotal
        print('{}/{} correct'.format(numCorrect, numTotal))
    print('{}/{} correct'.format(totalNumCorrect, totalTotal))
'''
    for tpl in terms.keys():
        try:
            [pt,sol,term,nb,nw] = tpl
            print('pt={},sol={},term={},nb={},nw={},count={}'.format(pt,sol,term,nb,nw,terms[tpl]))
        except ValueError:
            x = 'VER'
'''
    #test_problem('C:/Users/jblackmore/Documents/Development/Rutgers/GoLD/problems/resplit/train/2k/17324.sgf', modelBtL, None)
    #test_problem('C:/Users/jblackmore/Documents/Development/Rutgers/GoLD/problems/resplit/train/25k/3052.sgf')
    #test_problem('C:/Users/jblackmore/Documents/Development/Rutgers/GoLD/problems/resplit/train/25k/8177.sgf')
    