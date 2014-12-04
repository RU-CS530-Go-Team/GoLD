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

class FeatureExtractor():

    def __init__(self):
        pass

    def init_feature_services(self, start, move, movePosition, isblack):
        feature_services = dict()
        globals_hash = globals()
        services = [s for s in FEATURE_SERVICES if s!='PatchExtractor']
        for service in services:
            feature_services[service] = globals_hash[service](start, move, movePosition, isblack)
            if service=='PatchExtractor':
                feature_services[service].setPatchSize(4)
        return feature_services

    def extract_features(self, start, move, movePosition, isblack):
        feature_services = self.init_feature_services(start, move, movePosition, isblack)
        features = dict()
        for fk in feature_services.keys():
            fe = feature_services[fk]
            featureValue = fe.calculate_feature()
            fvtype = type(featureValue)
            if fvtype == ListType:
                for i,v in enumerate(featureValue):
                    features['{}_{:2d}'.format(fe.name(),i+1)] = v
            elif fvtype in [IntType, FloatType, StringType, float64]:
                features[fe.name()] = featureValue
            elif fvtype == ndarray:
                for i,v in enumerate(featureValue):
                    # not sure this is how the feature should be output...
                    if( type(v)==ndarray ):
                        for j,vv in enumerate(v):
                            features['{}_{}_{}'.format(fe.name(),i+1,j+1)] = vv
                    else:        
                        features['{}_{}'.format(fe.name(),i+1)] = v
            else:
                raise Exception('{}: Unexpected type {}'.format(fk,fvtype))
        return features
       
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
        print(f)
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
                        outcome=0
                        if isBTL == saysblack:
                            #CHECK THIS LOGIC
                            if mid in sn:
                                outcome = 1
                            elif mid in inc:
                                outcome = 0
                            else:
                                raise Exception('Unknown outcome!')
                        ''' Assume all moves for the "antagonist" are correct 
                        else:
                             Assume only moves on incorrect path are correct
                                for the "antagonist" <==> bad for the "protagonist" 
                            if mid in inc:
                                outcome = 0
                             Assume all moves for the "antagonist" are correct '''
                            # outcome = 1 '''
                        #features = features + fe.extract_features(start, move, (move_x, move_y), saysblack,outcome)
                        features = fe.extract_features(start, move, (move_x, move_y), saysblack)
                        inSoln = 1 if mid in sn else 0
                        inInc  = 1 if mid in inc else 0
                        isTerminal = 1 if i==len(path)-1 else 0
                        features['PT'] = probtyp
                        features['SOLUTION'] = inSoln
                        features['INC'] = inInc
                        features['TERM'] = isTerminal
                        features['PROBID'] = probId
                        features['DI'] = difficulty
                        features['MOVE'] = mid
                        features['PARENT'] = parent
                        movesConsidered.add((parent, mid))
                        vectors.append(features)
                        # Only train on the first wrong move for the protagonist
                        #if outcome==0 and isBTL==saysblack:
                        #    break;
                except IllegalMove as e:
                    print('{} ({},{}): {}'.format(fname, e, move_x, move_y))
                parent = mid
                start = move
        return vectors

    def get_vectors_from_fileOLD(self, f):
        #print(f)
        mtp = MoveTreeParser(f)
        #print('{} := {}'.format(f.split('/')[-1].split('\\')[-1], mtp.problemType))
        sn = mtp.getSolutionNodes()
        ss = mtp.getSolutionStates()
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
                        features.append(int(mid in ss))
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
                newf = subpaths[-1]+'features.csv'
                #newf2 = subpaths[-1]+'featuresWtK.csv'
                print('writing to {}'.format(newf))
                #print('writing to {}'.format(newf2))
                fout=open(newf, 'w')
                #fout2=open(newf2, 'w')
                #fout.write('ST_CNT,LIB,DFC,SOLUTION\n') #Removed CLR label until color feature readded
                #fout2.write('ST_CNT,LIB,DFC,SOLUTION\n') #Removed CLR label until color feature readded
                #csvwriter = csv.writer(fout)
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


if __name__ == '__main__':
    MoveTrainer(sys.argv[1:]).train()
