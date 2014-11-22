'''
Created on Nov 22, 2014

@author: JBlackmore
'''
from glob import glob
import sys
import os
from gold.extraneous.MoveTreeParser import MoveTreeParser
from gold.ui.Launcher import Launcher

class MoveTrainer():
    
    def __init__(self, baseDir):
        self.baseDir = baseDir

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
       
    def train(self):
        if os.path.isdir(self.baseDir):
            for f in self.file_search(self.baseDir):
                print('parsing {}'.format(f))
                mtp = MoveTreeParser(f)
                mtp.printAllPaths()
                print('=-=-===-=-=-===-=-=-===-=-=-===-=-=-===-=-=')
        else:
            mtp = MoveTreeParser(self.baseDir)
            ui = Launcher(400,400,50,mtp.start.x)
            ui.setBoard(mtp.start)
            ui.drawBoard()
            ui.mainloop()
            #mtp.printAllPaths()
            print('=-=-===-=-=-===-=-=-===-=-=-===-=-=-===-=-=')
if __name__ == '__main__':
    MoveTrainer(sys.argv[1]).train()