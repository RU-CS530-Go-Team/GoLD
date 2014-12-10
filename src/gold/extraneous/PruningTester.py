import sys
sys.path.append("/Users/zacharydaniels/Documents/GoLD/src/")

from gold.extraneous.MoveTreeParser import MoveTreeParser,\
    UnspecifiedProblemType
from gold.models.board import Board, IllegalMove
from random import seed, shuffle
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
    wa = 0
    wb = 0
    print('{}: w={}, b={}, wa={}, wb={}, nw={}, nb={}'.format(label,w,b,wa,wb,len(move.white_stones),len(move.black_stones)))

def test_problem(probfile, modelBtL, modelWtK):
    print(probfile)
    mtp = MoveTreeParser(probfile)
    ss = mtp.getSolutionPaths()
    isblack = mtp.blackFirst != mtp.flipColors
    move = mtp.start.clone()
    solutionStates = set()
    terminalIncorrectStates = set()
    solutionNodes = set()
    print_move('start ({}x{})'.format(move.x, move.y), move)
    longestPath = 0
    isBtL = (mtp.problemType == 1 or mtp.problemType==3)
    print(mtp.getProblemTypeDesc()+' - black={}, isBtL={}'.format(isblack, isBtL))
    for spath in ss:
        pathLength = 0
        move = mtp.start.clone()
        for step in spath:
            pathLength += 1
            if pathLength>longestPath:
                longestPath = pathLength
            fm = mtp.formatMove(mtp.moveID[step])
            move.place_stone(fm['x'], fm['y'], fm['isBlack'])
            color = 'B' if fm['isBlack'] else 'W'
            print_move('{}({},{})'.format(color,fm['x'],fm['y']), move)
            solutionNodes.add(move.clone())
            if step in mtp.getSolutionStates():
                solutionStates.add(move.clone())

        print('------------')

    move = mtp.start.clone()
    solutionNodes.add(move.clone())
    pathLength = 0

    end = False

    correctMoves = []

    print move

    while not end:

        predictedMoves = []
        notPredictedMoves = []

        end = True

        if isblack:
            mmt = MinMaxTree(move, True, not isBtL, blackModel=modelBtL, whiteModel=modelWtK, level=float('Inf'))
        else:
            mmt = MinMaxTree(move, False, isBtL, blackModel=modelBtL, whiteModel=modelWtK, level=float('Inf'))
        nextMoves = mmt.find_valid_moves()

        for moveData in nextMoves:
            if moveData['prob'] >= 0.0:
                predictedMoves.append(moveData['board'].clone())
            else:
                notPredictedMoves.append(moveData['board'].clone())
            if moveData['board'] in solutionNodes and moveData['prob'] >= 0.0:
                end = False
                correctMoves.append({'board': moveData['board'].clone(), 'isblack': not isblack, 'path':pathLength+1})
                print moveData['board']

        print len(predictedMoves)
        print len(notPredictedMoves)
        if len(correctMoves) == 0:
          end = True
        elif move in solutionStates:
          print "Win!"
          break
        else:
          moveTemp = correctMoves.pop()
          move = moveTemp['board']
          isblack = moveTemp['isblack']
          pathLength = moveTemp['path']

    '''while(move in solutionNodes):
        color = 'B' if isblack else 'W'
        mmt = mmt.decideNextMove()
        move.place_stone(mmt.i, mmt.j, isblack)
        print_move('{}({},{})'.format(color,mmt.i, mmt.j), move)
        mmt.promote()
        if move in terminalIncorrectStates:
            raise 'Haha! You lose!'
        if move in solutionStates:
            print('{}: You Win!!'.format(probfile))
            return
        pathLength = pathLength+1
        isblack = not isblack
    raise Exception('Too many moves, you lose!!')'''
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
    problemDir = sys.argv[2]
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
    numCorrect = 0
    numTotal = 0
    seed(1234567890)
    if not os.path.isdir(problemDir):
        test_problem(problemDir, modelBtL, modelWtK)
        sys.exit()
    dirs = glob(problemDir+'/*')
    shuffle(dirs)
    for probdiff in dirs:
        if os.path.isdir(probdiff):
            files = glob(probdiff+'/*.sgf')
            for probfile in files:

                print(probfile)
                try:
                    test_problem(probfile, modelBtL, modelWtK)
                    numCorrect += 1
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
                    test_problem(probdiff, modelBtL, modelWtK)
                except UnspecifiedProblemType:
                    x= 'UPT'
                except IllegalMove as im:
                    print(im)
                except Exception as e:
                    print(e)
                    x = 'WHATEVER'
    print('{}/{} correct'.format(numCorrect, numTotal))
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
