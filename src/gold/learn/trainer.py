'''
Created on Nov 22, 2014

@author: JBlackmore
'''
from glob import glob
import sys
import os
import time
#import csv 
from gold.extraneous.MoveTreeParser import MoveTreeParser
from gold.models.board import Board, IllegalMove
from gold.features.StoneCountFeature import StoneCountFeature
from gold.features.DiffLiberties import DiffLiberties
from gold.features.DistanceFromCenterFeature import DistanceFromCenterFeature
from gold.features.ColorFeature import ColorFeature

class FeatureExtractor():
    
    def __init__(self):
        pass
    
    def extract_features(self, start, move, movePosition, isblack):
        if( not isblack ):
            newstart = Board(start.x, start.y)
            newstart.black_stones = start.white_stones
            newstart.white_stones = start.black_stones
            start = newstart
            newmove = Board(move.x, move.y)
            newmove.black_stones = move.white_stones
            newmove.white_stones = move.black_stones
            move = newmove
            isblack = True
        #x0 = ColorFeature(start, move, movePosition, isblack).calculate_feature()
        x1 = StoneCountFeature(start, move, movePosition, isblack).calculate_feature()
        x2 = DiffLiberties(start, move, movePosition, isblack).calculate_feature()
        x3 = DistanceFromCenterFeature(start, move, movePosition, isblack).calculate_feature()
        return [x1, x2, x3]
        
class MoveTrainer():
    
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
    
    def get_vectors_from_file(self, f):
        #print(f)
        mtp = MoveTreeParser(f)
        print('{} := {}'.format(f.split('/')[-1].split('\\')[-1], mtp.problemType))
        sn = mtp.getSolutionNodes()
        inc = mtp.getIncorrectNodes()
        pt = mtp.problemType
        isBTL = (pt==1 or pt==3)
        if not sn.isdisjoint(inc):
            print('NOT DISJOINT')
        paths = mtp.getAllPaths()
        movesConsidered = set()
        fe = FeatureExtractor()
        vectors = []
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
                    if (parent, mid) not in movesConsidered and isBTL == saysblack :
                        outcome = 0
                        if mid in sn:
                            outcome = 1
                        elif mid in inc:
                            outcome = 0
                        else:
                            raise Exception('Unknown outcome!')
                        features = fe.extract_features(start, move, (move_x, move_y), saysblack)
                        features.append(outcome)
                        #print('{}'.format(features))
                        movesConsidered.add((parent, mid))
                        vectors.append(features)
                        # Only train on the first wrong move
                        if outcome==0:
                            break;
                except IllegalMove as e:
                    print('{}: ({},{})'.format(e, move_x, move_y))
                parent = mid
                start = move
        return vectors
    
    def train(self):
        start = time.clock()
        for ldir in self.dirs:
            if os.path.isdir(ldir):
                subpaths = ldir.split('\\')
                #newf = '/'.join(subpaths[:-2])+'/'+subpaths[-1]+'.csv'
                newf = subpaths[-1]+'.csv'
                print('writing to {}'.format(newf))
                fout=open(newf, 'w') 
                fout.write('ST_CNT,LIB,DFC,SOLUTION\n')
                #csvwriter = csv.writer(fout)
                for f in self.file_search(ldir):
                    try:
                        v = self.get_vectors_from_file(f)
                        for xv in v:
                            fout.write(','.join([str(x) for x in xv]))
                            fout.write('\n')
                            #csvwriter.writerow(xv)
                        print('{} vectors in {}'.format(len(v), f))
                    except TypeError as te:
                        print(te)
                    except Exception as e:
                        #print('Unexpected Error: {}'.format(sys.exc_info()[0]))
                        print('Unexpected Error: {}'.format(e))
                        subpaths = f.split('/')
                        newf = '/'.join(subpaths[:-2])+'/discard/'+subpaths[-1].split('\\')[-1]
                        #print('Move {} to {}'.format(f, newf))
                        #raise
                fout.close()
            else:
                self.get_vectors_from_file(ldir)
    
                #ui = Launcher(400,400,50,mtp.start.x)
                #ui.setBoard(mtp.start)
                #ui.drawBoard()
                #ui.mainloop()
                #mtp.printAllPaths()
                print('=-=-===-=-=-===-=-=-===-=-=-===-=-=-===-=-=')
            end = time.clock()
            intvl = end - start
            print('Feature extraction took %.03f seconds' %intvl)
if __name__ == '__main__':
    MoveTrainer(sys.argv[1:]).train()