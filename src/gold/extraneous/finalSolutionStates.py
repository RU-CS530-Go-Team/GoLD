from glob import glob
import sys
import os
import time
from gold.extraneous.MoveTreeParser import MoveTreeParser
from gold.models.board import Board, IllegalMove

class SolutionStateParser():

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
        print sn
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
                            print mid
                            print move
                except IllegalMove as e:
                    print('{}: ({},{})'.format(e, move_x, move_y))
                parent = mid
                start = move

    def getStates(self):
        start = time.clock()
        for ldir in self.dirs:
            if os.path.isdir(ldir):
                for f in self.file_search(ldir):
                    try:
                        self.actOnSolutionStates(f)
                    except TypeError as te:
                        print(te)
                    except Exception as e:
                        print('Unexpected Error: {}'.format(e))
            else:
                self.actOnSolutionStates(ldir)
                print('=-=-===-=-=-===-=-=-===-=-=-===-=-=-===-=-=')
            end = time.clock()
            intvl = end - start
            print('Building solution boards took %.03f seconds' %intvl)
if __name__ == '__main__':
    SolutionStateParser(sys.argv[1:]).getStates()
