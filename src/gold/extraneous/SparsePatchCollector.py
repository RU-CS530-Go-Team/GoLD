from glob import glob
import sys
import os
import time
from gold.extraneous.MoveTreeParser import MoveTreeParser
import gold.extraneous.terminalLife
from gold.models.board import Board, IllegalMove
from gold.features.StoneCountFeature import StoneCountFeature
from gold.features.DiffLiberties import DiffLiberties
from gold.features.DistanceFromCenterFeature import DistanceFromCenterFeature
from gold.features.ColorFeature import ColorFeature
from gold.features.numberLiveGroups import numberLiveGroups
from gold.features.LocalShapesFeature import LocalShapesFeature
from gold.features.PatchExtractor import PatchExtractor
from gold.features.SparseDictionaryFeature import SparseDictionaryFeature
import numpy as np
import pickle

class SparsePatchCollector():

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

    def individualExtraction(self, start, move, movePosition, isblack,outcome):
        if( not isblack ):
            newstart = Board(start.x, start.y)
            newstart.black_stones = start.white_stones
            newstart.white_stones = start.black_stones
            start = newstart
            newmove = Board(move.x, move.y)
            newmove.black_stones = move.white_stones
            newmove.white_stones = move.black_stones
            move = newmove

        sparsePatches = SparseDictionaryFeature(start, move, movePosition, isblack).get_transformed_data(4,'features/')

        if isblack:
            for row in sparsePatches:
                self.fout1a.write(','.join([str(x) for x in row] + [str(outcome)]))
                self.fout1a.write('\n')

        else:
            for row in sparsePatches:
                self.fout2a.write(','.join([str(x) for x in row] + [str(outcome)]))
                self.fout2a.write('\n')

        sparsePatches = SparseDictionaryFeature(start, move, movePosition, isblack).get_transformed_data(5,'features/')

        if isblack:
            for row in sparsePatches:
                self.fout3a.write(','.join([str(x) for x in row] + [str(outcome)]))
                self.fout3a.write('\n')

        else:
            for row in sparsePatches:
                self.fout4a.write(','.join([str(x) for x in row] + [str(outcome)]))
                self.fout4a.write('\n')


    def extractPatches(self, f):
        mtp = MoveTreeParser(f)
        #print('{} := {}'.format(f.split('/')[-1].split('\\')[-1], mtp.problemType))
        sn = mtp.getSolutionNodes()
        inc = mtp.getIncorrectNodes()
        probtyp = mtp.getProblemType()
        if probtyp == 1 or probtyp == 3: #Black to live
            probtyp = 1
        elif probtyp == 2 or probtyp == 4: #White to kill
            probtyp = 2
        else: #Error should be thrown, but just in case it isn't
            probtyp = 0
        isBTL = (probtyp==1)
        if not sn.isdisjoint(inc):
            print('NOT DISJOINT')
        paths = mtp.getAllPaths()
        movesConsidered = set()
        for path in paths:
            parent = 0
            start = mtp.start
            #print('START NEW PATH')
            for mid in path:
                move_dict = mtp.formatMove(mtp.moveID[mid])
                saysblack = move_dict['isBlack'] #move_str[0:1]=='B'
                #print('{}''s turn'.format('black' if saysblack else 'white'))
                move_y = move_dict['y'] #ord(move_str[2]) - ord('a')
                move_x = move_dict['x'] #ord(move_str[3]) - ord('a')
                move = Board(start.x, start.y)
                move.white_stones = [x for x in start.white_stones]
                move.black_stones = [y for y in start.black_stones]
                try:
                    move.place_stone(move_x, move_y, saysblack)
                    if (parent, mid) not in movesConsidered:
                        outcome = 0
                        if isBTL == saysblack:
                            #CHECK THIS LOGIC
                            if mid in sn:
                                outcome = 1
                            elif mid in inc:
                                outcome = 0
                            else:
                                raise Exception('Unknown outcome!')
                        else:
                            ''' Assume only moves on incorrect path are correct
                                for the "antagonist" '''
                            if mid in inc:
                                outcome = 1
                            ''' Assume all moves for the "antagonist" are correct '''
                            # outcome = 1
                        self.individualExtraction(start, move, (move_x, move_y), saysblack,outcome)
                        movesConsidered.add((parent, mid))
                        # Only train on the first wrong move for the protagonist
                        if outcome==0 and isBTL==saysblack:
                            break;
                except IllegalMove as e:
                    print('{}: ({},{})'.format(e, move_x, move_y))
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
        self.fout1a=open('extraneous/games/sparsePatches4BtL.csv', 'w')
        self.fout2a=open('extraneous/games/sparsePatches4WtK.csv', 'w')
        self.fout3a=open('extraneous/games/sparsePatches5BtL.csv', 'w')
        self.fout4a=open('extraneous/games/sparsePatches5WtK.csv', 'w')
        start = time.clock()
        for ldir in self.dirs:
            if os.path.isdir(ldir):
                for f in self.file_search(ldir):
                    print f
                    try:
                        self.extractPatches(f)
                    except TypeError as te:
                        print(te)
                    except Exception as e:
                        print('Unexpected Error: {}'.format(e))
            else:
                self.actOnSolutionStates(ldir)
                print('=-=-===-=-=-===-=-=-===-=-=-===-=-=-===-=-=')
            end = time.clock()
            intvl = end - start
            print('Building database took %.03f seconds' %intvl)
        self.fout1a.close()
        self.fout2a.close()
        self.fout3a.close()
        self.fout4a.close()

if __name__ == '__main__':
    TerminalDatabase(sys.argv[1:]).getStates()
