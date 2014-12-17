'''
Created on Nov 28, 2014

@author: JBlackmore
'''
import time
from os.path import isfile, isdir

import csv
import argparse

from gold.ui.Launcher import Launcher
from gold.models.MoveTreeParser import MoveTreeParser, UnspecifiedProblemType
from gold.models.board import IllegalMove
from gold.models.search import MinMaxTree
from gold.models.life import determineLife
from gold.learn.Model import Model
from glob import glob

class YouLoseException(Exception):
    def __init__(self, value, path=None, maxnodecount=None):
        self.value = value
        self.path = path
        self.maxnodecount=maxnodecount
        
    def __str__(self):
        return repr(self.value)
    
def print_move(label, move, sw=None, sb=None, w=None, b=None, moves=None, prob=None, etime=None, nodecount=None):
    if w is None:
        liveWGr = determineLife(move, False)
        w = len(liveWGr)
    if b is None:
        liveBGr = determineLife(move, True)
        b = len(liveBGr)
    if prob is None:
        probS=''
    elif prob>=5.0:
        probS = ' T'
    else:
        probS = ' {:.3f}'.format(prob)
    if etime is None:
        timeS = ''
    else:
        timeS = ' ({:.1f} seconds).'.format(etime)
        if nodecount is not None:
            timeS = ' ({} moves, {:.1f} seconds, {} nodes).'.format(moves, etime, nodecount)
            
    if sw is None or sb is None:
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

def translate_dimensions_to_sgf(stone, xmin, xmax, ymin, ymax):
    x = stone[0]+int(xmin)
    y = stone[1]+int(ymin)
    xc = chr(ord('a')+x)
    yc = chr(ord('a')+y)
    coord_string = '{}{}'.format(yc,xc)
    return coord_string

def write_problem(results_dir, mtp, problemId, probtype, difficulty, path, result):
    fname = '{}/{}-result.sgf'.format(results_dir, problemId)
    pout = open(fname, 'w')
    #mtp =MoveTreeParser(gameFile)
    [xmin, xmax] = [mtp.boardDimensions["xMin"],mtp.boardDimensions["xMax"]]
    [ymin, ymax] = [mtp.boardDimensions["yMin"],mtp.boardDimensions["yMax"]]
    board = mtp.start
    pout.write('(;GE[life and death]DI[{}]DP[{}]SO[xxxx]CO[9]'.format(difficulty, len(path)))
    for color,stones in [['W',board.white_stones], ['B',board.black_stones]]:
        for stone in stones:
            coord_string = translate_dimensions_to_sgf(stone, xmin, xmax, ymin, ymax)
            pout.write('A{}[{}]'.format(color, coord_string))
    pout.write('C[black to live]AP[gold]\n(')
    white = mtp.start.white_stones
    black = mtp.start.black_stones
    for move in path[1:]:
        new_white = [x for x in move.white_stones if x not in white]
        new_black = [x for x in move.black_stones if x not in black]
        white = move.white_stones
        black = move.black_stones
        if len(new_white)==1:
            pout.write(';W[{}]'.format(translate_dimensions_to_sgf(new_white[0], xmin, xmax, ymin, ymax)))
        elif len(new_black)==1:
            pout.write(';B[{}]'.format(translate_dimensions_to_sgf(new_black[0], xmin, xmax, ymin, ymax)))
        else:
            raise ValueError('I expected either 1 new white piece or 1 new black piece.')
    if result==0:
        res_str = 'Too many moves, you lose!!'
    elif result>0:
        res_str = 'You win!! Black has groups that are unconditionally alive! RIGHT'
    pout.write('C[GoLD result: {}]))'.format(res_str))
    pout.close()

    
def test_problem(mtp, modelBtL, modelWtK, maxdepth=10):
    [solutionStates, terminalIncorrectStates, longestPath] = get_terminal_states(mtp)

    move = mtp.start.clone()
    isBtL = (mtp.problemType == 1 or mtp.problemType==3)
    if not isBtL:
        raise UnspecifiedProblemType('Only configured to test black-to-live problems')
    sb = len(determineLife(mtp.start, True))
    sw = len(determineLife(mtp.start, False))
    pathLength = 0
    isblack = mtp.blackFirst != mtp.flipColors
    path = [move.clone()]
    print('GOLD:')
    start = time.clock()
    mmt = MinMaxTree(move, isblack, not isblack, blackModel=modelBtL, whiteModel=modelWtK)        
    mmt.extend_tree()
    passed = False
    maxpathlength = 2*longestPath+3
    maxnodecount=0
    while( move not in solutionStates and pathLength<maxpathlength):
        color = 'B' if isblack else 'W'
        moves=len(mmt.children)
        validMove = False
        illegalMoves = set()
        while not validMove:
            nextMove = mmt.decideNextMove()
            if nextMove is None:
                print('Pass.')
                if passed:
                    if mmt.terminal:
                        print('Two passes and Black lives. You win!!')
                        return [path,maxnodecount]
                    raise YouLoseException('Two passes in a row. You Lose!', path,maxnodecount)
                passed=True
                continue
            elif passed:
                passed =False
            try:
                move.place_stone(nextMove.i, nextMove.j, mmt.isblack)
                validMove=True
            except IllegalMove as im:
                # Rebuild that part of the tree
                # and prune away the illegal moves
                print('({},{}): {}'.format(nextMove.i,nextMove.j,im))
                [i,j] = [nextMove.i,nextMove.j]
                mmt.prune((i,j))
                illegalMoves.add((i,j))
                mmt.promote(extendIfSame=True)
                for p,q in illegalMoves:
                    mmt.prune((p,q))
                nextMove = None
        if nextMove.value is None: 
            if nextMove.terminal:
                prob = 5.0
            else:
                prob = nextMove.value +10.0
        else:
            prob = nextMove.value
        nodecount = mmt.node_count()
        if nodecount>maxnodecount:
            maxnodecount=nodecount
        print_move('{}({},{})'.format(color,nextMove.i, nextMove.j), move, sb=sb, sw=sw, moves=moves,prob=prob, etime=time.clock()-start, nodecount=nodecount)
        start = time.clock()        
        mmt = nextMove
        
        path.append(move.clone())

        if move in terminalIncorrectStates:
            raise YouLoseException('Haha! You lose!', path, maxnodecount)
        if move in solutionStates:
            print('Solution matched!! You Win!! ')
            return [path, maxnodecount]
        if mmt.sb is None:
            mmt.sb = len(determineLife(mmt.board,isblack))
        if mmt.sb>sb:
            print('You win!!! Black has groups that are unconditionally alive!')
            return [path, maxnodecount]
        pathLength = pathLength+1
        if pathLength<maxpathlength:
            mmt.promote()
        isblack = not isblack
            
    raise YouLoseException('Too many moves, you lose!!', path, maxnodecount)
        

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

def call_test_problem(probfile, modelBtL, modelWtK, outputfile=None, skip=set(), show=False, results_dir=None):
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
    start = time.clock()

    try:
        mtp = MoveTreeParser(probfile) 
        isBtL = (mtp.problemType == 1 or mtp.problemType==3)
        if not isBtL:
            return -1
        problemType = '1'
        print probfile
        start = time.clock()
        [path, maxnodecount] = test_problem(mtp, modelBtL, modelWtK)
        result= 1
    except UnspecifiedProblemType:
        result= -1
    except IllegalMove as im:
        print(im)
        result= -1
    except YouLoseException as yle:
        print(yle)
        path = yle.path
        maxnodecount = yle.maxnodecount
        result= 0
    if result>=0:
        if outputfile is not None:
            etime = time.clock()-start
            fout = open(outputfile, 'a')
            fout.write('{},{},{},{},{},'.format(problemId, problemType,difficulty,mtp.start.x, mtp.start.y))
            fout.write('{},{},{},'.format('BEAMN', MinMaxTree.maxdepth, MinMaxTree.beamsize))
            fout.write('{},{},{:.1f},{}\n'.format(len(path)-1, maxnodecount,etime, result))
            fout.close()
            #print('Writing results to {}'.format(results_dir))
            write_problem(results_dir, mtp,problemId, problemType, difficulty, path, result)
        if show:
            ui = Launcher(400,400,50,max(mtp.start.x, mtp.start.y))
            ui.showPath(path)
    return result
            
def load_model(modelFile, modelType, scalerFile):
    model = Model(modelFile, modelType)
    model.setScaler(scalerFile)
    return model

def test_problems(modelBtl, modelWtK, probdirs, outputfile, rerun=False, maxdepth=3, show=False, results_dir=None):
    
    #test_problem(sys.argv[1], modelBtL, modelWtK)
    MinMaxTree.maxdepth=maxdepth
    problemsDone = set()
    header = 'PROBLEM,TYPE,DIFFICULTY,X,Y,SEARCH,DEPTH,BEAM,MOVES,MAXNODES,TIME,RESULT'
    if not rerun:
        try:
            with open(outputfile, 'r') as csvin: 
                rdr = csv.reader(csvin)
                for row in rdr:
                    problemsDone.add(row[0])
        except Exception as e:
            print(e)
            with open(outputfile, 'w') as fout:
                fout.write('{}\n'.format(header))
                
    elif not isfile(outputfile):
        with open(outputfile, 'w') as fout:
            fout.write('{}\n'.format(header))
                    
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
                result = call_test_problem(problemDir, modelBtL, modelWtK, outputfile, skip=problemsDone, show=show, results_dir=results_dir)
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
            for probdiff in dirs:
                if isdir(probdiff):
                    files = glob(probdiff+'/*.sgf')
                    for probfile in files:
                        
                        result = call_test_problem(probfile, modelBtL, modelWtK, outputfile, skip=problemsDone, show=show, results_dir=results_dir)
                        if result>=0:
                            numTotal+=1
                            if result>0:
                                numCorrect+=1
                    if result!=-1:
                        print('{}: {}/{} correct'.format(probdiff, numCorrect, numTotal))
                        
                else:
                    if probdiff[-3:]=='sgf':
                        result = call_test_problem(probdiff, modelBtL, modelWtK, outputfile, skip=problemsDone,show=show, results_dir=results_dir)
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
    parser.add_argument('--results_dir', default=None, help='Directory for writing resulting path to .sgf files', required=False)
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
    print('Loading model and scaler files from {}...'.format(modelDir))
    problemDirs = args.problem_dir_or_file

    MinMaxTree.beamsize = args.beam_size
    
    if args.output_file is None:
        outputfile = modelDir+'/problem-test-results.txt'
    else:
        outputfile = args.output_file
    if args.results_dir is None or args.results_dir=='None':
        resultsdir = modelDir
    else:
        resultsdir = args.results_dir
    print('Setting results_dir to {}'.format(resultsdir))
    test_problems(modelBtL, modelWtK, problemDirs, outputfile, rerun=args.rerun_problems, maxdepth=args.max_depth, show=args.show_board, results_dir=resultsdir)
    