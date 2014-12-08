'''
Created on Nov 28, 2014

@author: JBlackmore
'''
from gold.extraneous.MoveTreeParser import MoveTreeParser,\
    UnspecifiedProblemType
from gold.models.board import IllegalMove
from random import seed, shuffle
import sys
import os
from gold.models.search import MinMaxTree
from gold.extraneous.life import determineLife
from gold.learn.Model import Model
from glob import glob

class YouLoseException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
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
    sb = len(determineLife(mtp.start, True))
    print('SOLUTIONS:')
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
        if move in terminalIncorrectStates:
            raise YouLoseException('Haha! You lose!')
        if move in solutionStates:
            print('{}: You Win!!'.format(probfile))
            return
        b = len(determineLife(move, True))
        if b>sb and isBtL:
            print('You Win!!! Black has {} groups that are unconditionally alive!'.format(b))
            return
        pathLength = pathLength+1
        if pathLength>=2*longestPath:
            raise YouLoseException('Too many moves, you lose!!')
            
        isblack = not isblack
        mmt.promote()
    '''
    ui=Launcher(400,400,50,max(move.x,move.y))
    ui.setBoard(move)
    ui.drawBoard()
    ui.mainloop()
    '''
def parse_problem_filename(probfile):
    subpaths = probfile.split('/')
    if subpaths[-1].rfind('\\')>0:
        subsub = subpaths[-1].split('\\')
        problemId = subsub[-1]
        difficulty = subsub[-2]
    else:
        difficulty= probfile.split('/')[-2]
        problemId = probfile.split('/')[-1]
    problemId = problemId.split('.')[-2]
    return [problemId, difficulty]

def call_test_problem(probfile, modelBtL, modelWtK, fout=None):
    ''' Returns 1 if problem is solved
        Returns 0 if problem could not be solved
        Returns -1 if problem could not be executed
    '''
    if probfile[-3:]=='sgf':
        [problemId, difficulty]=parse_problem_filename(probfile)
        #print(probdiff)
        try:
            test_problem(probfile, modelBtL, modelWtK)
            if fout is not None:
                fout.write('{},{},1\n'.format(problemId, difficulty))
            return 1
        except UnspecifiedProblemType:
            return -1
        except IllegalMove as im:
            print(im)
            return -1
        except YouLoseException as yle:
            print(yle)
            if fout is not None:
                fout.write('{},{},0\n'.format(problemId, difficulty))
            return 0
    else:
        raise Exception('{} is not a .sgf file'.format(probfile))
            
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

def test_problems(modelBtl, modelWtK, probdirs, outputfile):
    
    #test_problem(sys.argv[1], modelBtL, modelWtK)
    with open(outputfile, 'w') as fout:
        fout.write('PROBLEM,DIFFICULTY,SCORE\n')
        seed(1234567890)
        totalNumCorrect = 0
        totalTotal = 0
        for problemDir in probdirs:
            print problemDir
            numCorrect = 0
            numTotal = 0
            if not os.path.isdir(problemDir):
                if len(problemDir)<3:
                    print('Not a dir or problem file: {}'.format(problemDir))
                elif problemDir[-3]=='sgf':
                    result = call_test_problem(problemDir, modelBtL, modelWtK, fout)
                    if result>=0:
                        numTotal+=1
                        if result>0:
                            numCorrect+=1

                else:
                    print('Not a dir or problem file: {}'.format(problemDir))
                sys.exit()
            dirs = glob(problemDir+'/*')
            shuffle(dirs)
            for probdiff in dirs:
                if os.path.isdir(probdiff):
                    files = glob(probdiff+'/*.sgf')
                    for probfile in files:
                        
                        result = call_test_problem(probfile, modelBtL, modelWtK, fout)
                        if result>=0:
                            numTotal+=1
                            if result>0:
                                numCorrect+=1
                        
                else:
                    if probdiff[-3:]=='sgf':
                        result = call_test_problem(probdiff, modelBtL, modelWtK, fout)
                        if result>=0:
                            numTotal+=1
                            if result>0:
                                numCorrect+=1
                if result>=0:
                    print('{}/{} correct'.format(numCorrect, numTotal))

            totalNumCorrect+=numCorrect
            totalTotal+=numTotal
            print('{}/{} correct'.format(numCorrect, numTotal))
        print('{}/{} correct'.format(totalNumCorrect, totalTotal))
    

if __name__ == '__main__':
    if len(sys.argv)<3:
        print('Usage: python ProblemTester <model_dir> <problem_dir_or_file1> [problem_dir_or_file2...]')
        sys.exit()
    
    # Sample main... make your own if you want something different
    # Just import load_model and test_problems
    modelDir = sys.argv[1]
    modelFile = modelDir+'/modelNBBtL.txt'
    modelType = 3 
    scalerFile = modelDir+'/trainfeaturesBtLScaler.txt'
    modelBtL = load_model(modelFile, modelType, scalerFile)
    modelFile = modelDir+'/modelNBWtK.txt'
    modelType = 3
    scalerFile = modelDir+'/trainfeaturesWtKScaler.txt'
    modelWtK = load_model(modelFile, modelType, scalerFile)
    problemDirs = sys.argv[2:]

    outputfile = modelDir+'/problem-test-results.txt'
    test_problems(modelBtL, modelWtK, problemDirs, outputfile)
    