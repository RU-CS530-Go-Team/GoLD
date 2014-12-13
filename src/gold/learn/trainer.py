'''
Created on Nov 22, 2014

@author: JBlackmore
'''
import sys
import os
import time
import csv
from glob import glob
from numpy import ndarray, float64
from types import ListType, IntType, FloatType, StringType
from gold.extraneous.MoveTreeParser import MoveTreeParser, UnspecifiedProblemType
from gold.models.board import Board, IllegalMove
from gold.features import *
from gold.features.extractor import FeatureExtractor

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
        mtp = MoveTreeParser(f)
        #print('{} := {}'.format(f.split('/')[-1].split('\\')[-1], mtp.problemType))
        subpaths = f.split('/')
        subfnparts = subpaths[-1].split('\\')
        difficulty = subfnparts[-2]
        fname = subfnparts[-1]
        probId = fname.split('.')[0]
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
            for i,mid in enumerate(path):
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
                        features = fe.extract_features(start, move, (move_x, move_y), saysblack)
                        inSoln = 1 if mid in sn else 0
                        inInc  = 1 if mid in inc else 0
                        isTerminal = 1 if i==len(path)-1 else 0
                        features['_PT'] = probtyp
                        features['_SOLUTION'] = inSoln
                        features['_INC'] = inInc
                        features['_TERM'] = isTerminal
                        features['_PROBID'] = probId
                        features['_DI'] = difficulty
                        features['_MOVE'] = mid
                        features['_PARENT'] = parent
                        movesConsidered.add((parent, mid))
                        vectors.append(features)
                except IllegalMove as e:
                    print('{} ({},{}): {}'.format(fname, move_x, move_y, e))
                parent = mid
                start = move
        return vectors

    def train(self):
        start = time.clock()
        for ldir in self.dirs:
            if os.path.isdir(ldir):
                subpaths = ldir.split('\\')
                newf = subpaths[-1]+'features.csv'
                print('writing to {}'.format(newf))
                fout=open(newf, 'w')
                writer = None
                for f in self.file_search(ldir):
                    fname = f.split('/')[-1]
                    try:
                        v = self.get_vectors_from_file(f)
                        for xv in v:
                            if writer == None:
                                writer = csv.DictWriter(fout, xv.keys(), lineterminator='\n')
                                writer.writeheader()
                            writer.writerow(xv)
                        print('{} vectors in {}'.format(len(v), fname))
                    except TypeError as te:
                        print(te)
                    except UnspecifiedProblemType as upt:
                        error = upt
                        #print(error)
                    except Exception as e:
                        print('Unexpected Error: {}'.format(e))

                fout.close()
                #fout2.close()
            else:
                self.get_vectors_from_file(ldir)

            end = time.clock()
            intvl = end - start
            print('Feature extraction took %.03f seconds' %intvl)

''' merge csv2 into csv1 '''
def merge_csv(csv1, csv2, csv3=None):
    if csv3 == None:
        csv3 = csv1
    rows = []
    with open(csv1, 'r') as csvf1, open(csv2, 'r') as csvf2:
        rdr1 = csv.DictReader(csvf1)
        rdr2 = csv.DictReader(csvf2)
        f2values = {}
        headers = rdr1.fieldnames
        for row in rdr2:
            difficulty = row['_DI']
            pt = row['_PT']
            probid = row['_PROBID']
            moveid = row['_MOVE']
            key = '{}.{}.{}.{}'.format(difficulty,pt,probid,moveid)
            f2values[key]=row
        for row in rdr1:
            difficulty = row['_DI']
            pt = row['_PT']
            probid = row['_PROBID']
            moveid= row['_MOVE']
            key = '{}.{}.{}.{}'.format(difficulty,pt,probid,moveid)
            if key in f2values.keys():
                row.update(f2values.pop(key))
                rows.append(row)
            else:
                print('{}: no match found in {}'.format(key, csv2))
        for key in f2values.keys():
            print('{}: no match found in {}'.format(key, csv1))
        with open(csv3, 'w') as csvout:
            wtr = csv.DictWriter(csvout, headers, lineterminator='\n')
            wtr.writeheader()
            wtr.writerows(rows)

if __name__ == '__main__':
    MoveTrainer(sys.argv[1:]).train()
