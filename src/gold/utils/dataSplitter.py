'''
Created on Nov 17, 2014

@author: JBlackmore
'''
import glob
import os
import shutil

base = 'c:/users/jblackmore/documents/development/Rutgers/GoLD/problems'
def loadSet(set_type):
    infname = base+'/'+set_type+'Files.txt'
    with open(infname, 'r') as inf:
        setFiles = [x.rstrip() for x in inf.readlines()]
        return setFiles
    raise IOError('No files found for '+set_type)

def do_stuff():
    devSet = loadSet('dev')
    trainSet = loadSet('train')
    devDir = base+'/resplit/dev'
    trainDir = base+'/resplit/train'
    os.mkdir(devDir)
    os.mkdir(trainDir)
    for difficultyDir in glob.glob(base+'/splitByDifficulty/*'):
        difficulty = difficultyDir.split('\\')[-1]
        trainDiffDir = trainDir+'/'+difficulty 
        os.mkdir(trainDiffDir)
        devDiffDir = devDir+'/'+difficulty
        os.mkdir(devDiffDir)
        print(difficulty)
        for sgfFile in glob.glob(difficultyDir+'/*.sgf'):
            fname = sgfFile.split('\\')[-1]
            if fname in devSet:
                dest = devDiffDir+'/'+fname
                shutil.copy(sgfFile, dest)
            elif fname in trainSet:
                dest = trainDiffDir+'/'+fname
                shutil.copy(sgfFile, dest)

do_stuff()