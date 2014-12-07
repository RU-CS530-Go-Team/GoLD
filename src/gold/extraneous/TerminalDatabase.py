from glob import glob
import sys
import os
import time
from gold.extraneous.MoveTreeParser import MoveTreeParser
import gold.extraneous.terminalLife
from gold.models.board import Board, IllegalMove
import numpy as np
import pickle

class TerminalDatabase():

    def __init__(self, dirs):
        self.dirs = dirs

    ''' Who doesnt love depth-first search? '''
    def file_search(self, search_dir):
        files = []
        for f in glob(search_dir+'/*'):
            if os.path.isdir(f):
                for sf in self.file_search(f):
                    files.append(sf)
            else:
                files.append(f)
        return files

    def actOnSolutionStates(self, f):
        mtp = MoveTreeParser(f)
        print('{} := {}'.format(f.split('/')[-1].split('\\')[-1], mtp.problemType))
        sn = mtp.getSolutionStates()
        #print sn
        probtyp = mtp.getProblemType()
        if probtyp == 1 or probtyp == 3: #Black to live
            probtyp = 1
        elif probtyp == 2 or probtyp == 4: #White to kill
            probtyp = 2
        else: #Error should be thrown, but just in case it isn't
            probtyp = 0
        isBTL = (probtyp==1)
        paths = mtp.getSolutionPaths()
        for path in paths:
            parent = 0
            start = mtp.start
            for mid in path:
                move_dict = mtp.formatMove(mtp.moveID[mid])
                saysblack = move_dict['isBlack']
                move_y = move_dict['y']
                move_x = move_dict['x']
                move = Board(start.x, start.y)
                move.white_stones = [x for x in start.white_stones]
                move.black_stones = [y for y in start.black_stones]
                try:
                    move.place_stone(move_x, move_y, saysblack)
                    if isBTL == saysblack:
                        if mid in sn:
                            #DO WHATEVER YOU WANT WITH BOARD: move
                            moveConverted = self.convert_board(move,0,2)
                            print mid
                            print moveConverted
                            print move
                            print move.black_stones
                            print move.white_stones
                            aliveGroups = gold.extraneous.terminalLife.findAliveGroups(move, saysblack)
                            print aliveGroups
                except IllegalMove as e:
                    print('{}: ({},{})'.format(e, move_x, move_y,sys.exc_info()[-1].tb_lineno))
                parent = mid
                start = move

    def convert_board(self,boardInput,blankVal,edgeVal):
        boardOutput = np.zeros((boardInput.x+2,boardInput.y+2))
        for i in range(boardInput.x + 2):
            for q in range(boardInput.y + 2):
                if i == 0 or i == boardInput.x + 1 or q == 0 or q == boardInput.y + 1:
                    boardOutput[i][q] = edgeVal

        for i in range(boardInput.x):
            for q in range(boardInput.y):
                if (i, q) in boardInput.white_stones:
                    boardOutput[i+1][q+1] = -1
                elif (i, q) in boardInput.black_stones:
                    boardOutput[i+1][q+1] = 1
                else:
                    boardOutput[i+1][q+1] = blankVal
        return boardOutput

    def buildDatabase(self):
        start = time.clock()
        for ldir in self.dirs:
            if os.path.isdir(ldir):
                for f in self.file_search(ldir):
                    try:
                        self.actOnSolutionStates(f)
                    except TypeError as te:
                        print(te)
                    #except gold.extraneous.MoveTreeParser.UnspecifiedProblemType:
                        #pass
                    except Exception as e:
                        print('Unexpected Error: {}'.format(e))
            else:
                self.actOnSolutionStates(ldir)
                print('=-=-===-=-=-===-=-=-===-=-=-===-=-=-===-=-=')
            end = time.clock()
            intvl = end - start
            print('Building database took %.03f seconds' %intvl)
if __name__ == '__main__':
    TerminalDatabase(sys.argv[1:]).getStates()
