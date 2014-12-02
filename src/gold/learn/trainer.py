'''
Created on Nov 22, 2014

@author: JBlackmore
'''
from glob import glob
import sys
import os
import time
from gold.extraneous.MoveTreeParser import MoveTreeParser, UnspecifiedProblemType
from gold.models.board import Board, IllegalMove
from gold.features.StoneCountFeature import StoneCountFeature
from gold.features.DiffLiberties import DiffLiberties
from gold.features.DistanceFromCenterFeature import DistanceFromCenterFeature
from gold.features.ColorFeature import ColorFeature
from gold.features.numberLiveGroups import numberLiveGroups
from gold.features.LocalShapesFeature import LocalShapesFeature
from gold.features.PatchExtractor import PatchExtractor
from gold.features.SparseDictionaryFeature import SparseDictionaryFeature

class FeatureExtractor():

    def __init__(self):
        pass

    def extract_features(self, start, move, movePosition, isblack,outcome):
        x0 = ColorFeature(start, move, movePosition, isblack).calculate_feature()
        if( not isblack ):
            newstart = Board(start.x, start.y)
            newstart.black_stones = start.white_stones
            newstart.white_stones = start.black_stones
            start = newstart
            newmove = Board(move.x, move.y)
            newmove.black_stones = move.white_stones
            newmove.white_stones = move.black_stones
            move = newmove
        x1 = StoneCountFeature(start, move, movePosition, isblack).calculate_feature()
        x2 = DiffLiberties(start, move, movePosition, isblack).calculate_feature()
        x3 = DistanceFromCenterFeature(start, move, movePosition, isblack).calculate_feature()
        x4 = numberLiveGroups(start, move, movePosition, isblack).calculate_feature()
        #x5 = LocalShapesFeature(start, move, movePosition, isblack).calculate_feature(dataDir="features/")

        '''patchEx = PatchExtractor(start, move, movePosition, isblack)
        patchEx.setPatchSize(6)
        x6 = patchEx.calculate_feature()

        for row in x6:
          fout=open('extraneous/games/patches6.csv', 'a')
          fout.write(','.join([str(x) for x in row]))
          fout.write('\n')
          fout.close()'''

        #x6 = SparseDictionaryFeature(start, move, movePosition, isblack).calculate_feature(dataDir="../features/")

        #return x6
        #return [x0, x1, x2, x3, x4, x5]
        #return [x0, x1, x2, x3, x4, x5] + x6
        #return [x0, x1, x2, x3, x4] + x6
        #return [x0] + x5
        #return [x0] + x6
        return [x0] + x1 + x2 + [x3] + x4
        #return [0]

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
            elif f[-3:]=='sgf':
                files.append(f)
            else:
                print('Ignoring unrecognized file {}'.format(f.split('/')[-1]))
        return files

    def get_vectors_from_file(self, f):
        #print(f)
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
                    if (parent, mid) not in movesConsidered:
                        features = [probtyp]
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
                        features = features + fe.extract_features(start, move, (move_x, move_y), saysblack,outcome)
                        #features = fe.extract_features(start, move, (move_x, move_y), saysblack)
                        features.append(outcome)
                        movesConsidered.add((parent, mid))
                        vectors.append(features)
                        # Only train on the first wrong move for the protagonist
                        if outcome==0 and isBTL==saysblack:
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
                newf = subpaths[-1]+'featuresBtL.csv'
                newf2 = subpaths[-1]+'featuresWtK.csv'
                print('writing to {}'.format(newf))
                print('writing to {}'.format(newf2))
                fout=open(newf, 'w')
                fout2=open(newf2, 'w')
                fout.write('ST_CNT,LIB,DFC,SOLUTION\n') #Removed CLR label until color feature readded
                fout2.write('ST_CNT,LIB,DFC,SOLUTION\n') #Removed CLR label until color feature readded
                #csvwriter = csv.writer(fout)
                for f in self.file_search(ldir):
                    try:
                        v = self.get_vectors_from_file(f)
                        for xv in v:
                            probtyp = xv.pop(0)
                            movetyp = (xv.pop(0))==1
                            if (probtyp == 1 and movetyp) or (probtyp == 2 and not movetyp):
                                fout.write(','.join([str(x) for x in xv]))
                                fout.write('\n')
                            elif (probtyp == 1 and not movetyp) or (probtyp == 2 and movetyp):
                                fout2.write(','.join([str(x) for x in xv]))
                                fout2.write('\n')
                            #csvwriter.writerow(xv)
                        print('{} vectors in {}'.format(len(v), f.split('/')[-1]))
                    except TypeError as te:
                        print(te)
                    except UnspecifiedProblemType as upt:
                        error = upt
                        print(error)
                    except Exception as e:
                        print('Unexpected Error: {}'.format(e))

                fout.close()
                fout2.close()
            else:
                self.get_vectors_from_file(ldir)

            end = time.clock()
            intvl = end - start
            print('Feature extraction took %.03f seconds' %intvl)


if __name__ == '__main__':
    MoveTrainer(sys.argv[1:]).train()
