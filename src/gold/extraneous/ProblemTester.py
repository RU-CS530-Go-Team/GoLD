'''
Created on Nov 28, 2014

@author: JBlackmore
'''
import time
from os.path import isfile, isdir

import csv
import argparse

from gold.ui.Launcher import Launcher
from gold.extraneous.MoveTreeParser import MoveTreeParser,\
    UnspecifiedProblemType
from gold.models.board import IllegalMove
from random import seed, shuffle
from gold.models.search import MinMaxTree
from gold.extraneous.life import determineLife
from gold.extraneous.terminalLife import findAliveGroups
from gold.learn.Model import Model
#from gold.ui.Launcher import Launcher
from glob import glob

class YouLoseException(Exception):
    def __init__(self, value, path=None):
        self.value = value
        self.path = path

    def __str__(self):
        return repr(self.value)
    
def print_move(label, move, sw=-1, sb=-1, w=-1, b=-1, moves=None, prob=None, etime=None, nodecount=None):
    if w<0:
        liveWGr = determineLife(move, False)
        w = len(liveWGr)
    if b<0:
        liveBGr = determineLife(move, True)
        b = len(liveBGr)
    if prob is None:
        probS=''
    else:
        probS = ' {:.3f}'.format(prob)
    if etime is None:
        timeS = ''
    else:
        timeS = ' ({:.1f} seconds).'.format(etime)
        if nodecount is not None:
            timeS = ' ({} moves, {:.1f} seconds, {} nodes).'.format(moves, etime, nodecount)
            
    if sw<0 and sb<0:
        print('{}: w={}, b={}, nw={}, nb={}{}{}'.format(label,w,b,len(move.white_stones),len(move.black_stones),probS, timeS))
    else:
        print('{}: w={}, b={}, sw={}, sb={}, nw={}, nb={}{}{}'.format(label,w,b,sw,sb,len(move.white_stones),len(move.black_stones),probS,timeS))

def get_terminal_states(mtp):
    ss = mtp.getSolutionPaths()
    #isblack = mtp.blackFirst != mtp.flipColors
    move = mtp.start.clone()
    solutionStates = set()
    terminalIncorrectStates = set()
    print_move('start ({}x{})'.format(move.x, move.y), move)
    longestPath = 0
    isBtL = (mtp.problemType == 1 or mtp.problemType==3)
    ptdesc = mtp.getProblemTypeDesc()
    if mtp.flipColors:
        ptdesc += ' => '
        if isBtL:
            ptdesc+='Black to Live'
        else:
            ptdesc+='White to Kill'
    print(ptdesc)
    print('SOLUTIONS:')
    for spath in ss:
        pathLength = 0
        move = mtp.start.clone()
        sb = len(determineLife(mtp.start, True))
        sw = len(determineLife(mtp.start, False))
        for step in spath:
            pathLength += 1
            if pathLength>longestPath:
                longestPath = pathLength
            fm = mtp.formatMove(mtp.moveID[step])
            move.place_stone(fm['x'], fm['y'], fm['isBlack'])
            color = 'B' if fm['isBlack'] else 'W'
            print_move('{}({},{})'.format(color,fm['x'],fm['y']), move, sw=sw, sb=sb)
            if step in mtp.getTerminalStates():
                if step in mtp.getSolutionStates():
                    solutionStates.add(move.clone())
                else:
                    terminalIncorrectStates.add(move.clone())

        print('------------')
    return [solutionStates, terminalIncorrectStates, longestPath]

def test_problem(mtp, modelBtL, modelWtK, maxdepth=10):
    [solutionStates, terminalIncorrectStates, longestPath] = get_terminal_states(mtp)

    move = mtp.start.clone()
    sb = len(determineLife(mtp.start, True))
    sw = len(determineLife(mtp.start, False))
    pathLength = 0
    isblack = mtp.blackFirst != mtp.flipColors
    isBtL = (mtp.problemType == 1 or mtp.problemType==3)
    path = [move.clone()]
    print('GOLD:')
    start = time.clock()        
    if isblack:
        mmt = MinMaxTree(move, True, not isBtL, blackModel=modelBtL, whiteModel=modelWtK)
    else:
        mmt = MinMaxTree(move, False, isBtL, blackModel=modelBtL, whiteModel=modelWtK)
    mmt.extend_tree()
    passed = False
    while( move not in solutionStates and pathLength<2*longestPath+5):
        color = 'B' if isblack else 'W'
        if mmt.isblack != isblack:
            raise ValueError('Ahem!')
        nextMove = mmt.decideNextMove()
        if nextMove is None:
            print('Pass.')
            if passed:
                if isBtL and len(determineLife(move, True))>0:
                    print('Two passes and Black lives. You win!!')
                    return path
                raise YouLoseException('Two passes in a row. You Lose!', path)
            passed=True
            continue
        try:
            move.place_stone(nextMove.i, nextMove.j, isblack)
        except IllegalMove as im:
            print ('{}: decided it was the next move, no recovery.'.format(im))
            return path
        #b = len(determineLife(move,True))
        b = len(determineLife(move, True))
        w = len(determineLife(move, False))
        if nextMove.value is None: 
            if nextMove.terminal:
                prob = 5.0
            else:
                prob = nextMove.value +10.0
        else:
            prob = nextMove.value
        print_move('{}({},{})'.format(color,nextMove.i, nextMove.j), move, sb=sb, sw=sw, b=b, w=w, moves=len(mmt.children),prob=prob, etime=time.clock()-start, nodecount=mmt.node_count())
        mmt = nextMove
        path.append(move.clone())
        start = time.clock()        

        if move in terminalIncorrectStates:
            raise YouLoseException('Haha! You lose!', path)
        if move in solutionStates:
            print('Solution matched!! You Win!! ')
            return path
        if b>sb:
            if isBtL:
                print('You Win!!! Black has {} groups that are unconditionally alive!'.format(b))
                return path
            else:
                raise YouLoseException('Black lives!! You Lose!!', path)
        pathLength = pathLength+1
        if pathLength>=2*longestPath+5:
            if not isBtL:
                start = time.clock()
                print('Searching for black to live...')
                numAliveGroups= len(findAliveGroups(move, True))
                searchTime= time.clock()-start
                print('Search took {:1f} seconds. {} alive.'.format(searchTime, '{} groups are'.format(numAliveGroups) if numAliveGroups !=1 else '1 group is'))
                if searchTime>600.0:
                    if maxdepth>3:
                        maxdepth -=1
                        print('Reducing search depth to {}'.format(maxdepth))
                    else:
                        print('Search depth is already down to 3!')
                if numAliveGroups>0:
                    raise YouLoseException('Too many moves and black can live, you lose!!', path)
                print('You win!! Black is dead!')
                return path
            raise YouLoseException('Too many moves, you lose!!', path)
            
        isblack = not isblack
        mmt.promote()
            
    raise YouLoseException('Too many moves, you lose!!', path)
        

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

def call_test_problem(probfile, modelBtL, modelWtK, outputfile=None, skip=set(), show=False):
    ''' Returns 1 if problem is solved
        Returns 0 if problem could not be solved
        Returns -1 if problem could not be executed
    '''
    if probfile[-3:]!='sgf':
        raise Exception('{} is not a .sgf file'.format(probfile))

    [problemId, difficulty]=parse_problem_filename(probfile)
    if problemId in skip:
        print('Already did {} problem {}'.format(difficulty, problemId))
        return -1
    #print(probdiff)
    problemType = 'error'

    try:
        mtp = MoveTreeParser(probfile) 
        isBtL = (mtp.problemType == 1 or mtp.problemType==3)
        if not isBtL:
            return -1
        problemType = '1' if isBtL else '2'
        print probfile
        start = time.clock()
        path = test_problem(mtp, modelBtL, modelWtK)
        result= 1
    except UnspecifiedProblemType:
        result= -1
    except IllegalMove as im:
        print(im)
        result= -1
    except YouLoseException as yle:
        print(yle)
        path = yle.path
        result= 0
    if result>=0:
        if outputfile is not None:
            fout = open(outputfile, 'a')
            fout.write('{},{},{},{},{},'.format(problemId, problemType,difficulty,mtp.start.x, mtp.start.y))
            fout.write('{},{},{},'.format('BEAM1', MinMaxTree.maxdepth, MinMaxTree.beamsize))
            fout.write('{},{:.1f},{}\n'.format(len(path), time.clock()-start, result))
            fout.close()
        if show and result>=0:
            ui = Launcher(400,400,50,max(mtp.start.x, mtp.start.y))
            ui.showPath(path)
    return result
            
def load_model(modelFile, modelType, scalerFile):
    model = Model(modelFile, modelType)
    model.setScaler(scalerFile)
    return model

def test_problems(modelBtl, modelWtK, probdirs, outputfile, rerun=False, maxdepth=3, show=False):
    
    #test_problem(sys.argv[1], modelBtL, modelWtK)
    MinMaxTree.maxdepth=maxdepth
    problemsDone = set()
    if not rerun:
        try:
            with open(outputfile, 'r') as csvin: 
                rdr = csv.reader(csvin)
                for row in rdr:
                    problemsDone.add(row[0])
        except Exception as e:
            print(e)
            with open(outputfile, 'w') as fout:
                fout.write('PROBLEM,TYPE,DIFFICULTY,X,Y,SEARCH,DEPTH,BEAM,MOVES,TIME,RESULT\n')
                
    elif not isfile(outputfile):
        with open(outputfile, 'w') as fout:
            fout.write('PROBLEM,TYPE,DIFFICULTY,X,Y,SEARCH,DEPTH,BEAM,MOVES,TIME,RESULT\n')
                    
    #with open(outputfile, 'a') as fout:
    seed(1234567890)
    totalNumCorrect = 0
    totalTotal = 0
    for problemDir in probdirs:
        print problemDir
        numCorrect = 0
        numTotal = 0
        if not isdir(problemDir):
            if len(problemDir)<3:
                print('Not a dir or problem file: {}'.format(problemDir))
            elif problemDir[-3:]=='sgf':
                result = call_test_problem(problemDir, modelBtL, modelWtK, outputfile, skip=problemsDone, show=show)
                if result>=0:
                    numTotal+=1
                    if result>0:
                        numCorrect+=1
                if result!=-1:
                    print('Total: {}/{} correct'.format(numCorrect, numTotal))
            else:
                print('Not a dir or problem file: {}'.format(problemDir))

        else:
            dirs = glob(problemDir+'/*')
            shuffle(dirs)
            for probdiff in dirs:
                if isdir(probdiff):
                    files = glob(probdiff+'/*.sgf')
                    for probfile in files:
                        
                        result = call_test_problem(probfile, modelBtL, modelWtK, outputfile, skip=problemsDone, show=show)
                        if result>=0:
                            numTotal+=1
                            if result>0:
                                numCorrect+=1
                    if result!=-1:
                        print('{}: {}/{} correct'.format(probdiff, numCorrect, numTotal))
                        
                else:
                    if probdiff[-3:]=='sgf':
                        result = call_test_problem(probdiff, modelBtL, modelWtK, outputfile, skip=problemsDone)
                        if result>=0:
                            numTotal+=1
                            if result>0:
                                numCorrect+=1
                    if result!=-1:
                        print('{}: {}/{} correct'.format(problemDir, numCorrect, numTotal))

        totalNumCorrect+=numCorrect
        totalTotal+=numTotal
            
        print('Total: {}/{} correct'.format(totalNumCorrect, totalTotal))
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="", conflict_handler='resolve', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # rerun problems, 
    parser.add_argument('--rerun_problems', '-r', action='store_true', help='rerun problems already run') #default=False
    parser.add_argument('--max_depth', '-d', default='3', metavar='int', type=int, choices=[x+1 for x in range(5)], help='maximum depth to search for the next move')
    parser.add_argument('--output_file', '-o', help='output file', default=None, required=False)
    parser.add_argument('--show_board', '-s', action='store_true', help='Show the resulting path on the board when a problem is completed')
    parser.add_argument('--btl_model', '-b', default='RF100', help='Short name of machine learning model to use for black-to-live, e.g. if RF100, filename will be modelRF100BtL.txt')
    parser.add_argument('--wtk_model', '-w', default='RF100', help='Short name of machine learning model to use for white-to-kill, e.g. if RF100, filename will be modelRF100WtK.txt')
    parser.add_argument('--btl_model_type', default=1, type=int, required=False, choices=[0,1], help='BtL model type (0=SVM, 1=other)')
    parser.add_argument('--wtk_model_type', default=1, type=int, required=False, choices=[0,1], help='WtK model type (0=SVM, 1=other)')
    parser.add_argument('--beam_size', default=50, metavar='int', type=int, choices=[x+1 for x in range(100)], help='Breadth limit for top level search')
    parser.add_argument('model_dir', help='location of machine learning models')
    parser.add_argument('problem_dir_or_file', nargs='+', help='path to problem directory or file')
    args = parser.parse_args()
    
    
    # Sample main... make your own if you want something different
    # Just import load_model and test_problems
    modelDir = args.model_dir
    #modelFile = modelDir+'/modelNBBtL.txt'
    modelFile = modelDir+'/model'+args.btl_model+'BtL.txt'
    modelType = args.btl_model_type 
    scalerFile = modelDir+'/trainfeaturesBtLScaler.txt'
    modelBtL = load_model(modelFile, modelType, scalerFile)
    #modelFile = modelDir+'/modelNBWtK.txt'
    modelFile = modelDir+'/model'+args.wtk_model+'WtK.txt'
    modelType = args.wtk_model_type 
    scalerFile = modelDir+'/trainfeaturesWtKScaler.txt'
    modelWtK = load_model(modelFile, modelType, scalerFile)
    print('Loading model and scaler files...')
    problemDirs = args.problem_dir_or_file

    MinMaxTree.beamsize = args.beam_size
    
    if args.output_file is None:
        outputfile = modelDir+'/problem-test-results.txt'
    else:
        outputfile = args.output_file
    test_problems(modelBtL, modelWtK, problemDirs, outputfile, rerun=args.rerun_problems, maxdepth=args.max_depth, show=args.show_board)
    