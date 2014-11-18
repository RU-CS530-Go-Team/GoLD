'''
Created on Nov 17, 2014

@author: JBlackmore
'''
from Feature import Feature

class StoneCountFeature(Feature):
    '''
    classdocs
    '''
    def calculate_feature(self):
        blackdiff = len(self.move.black_stones)-len(self.start.black_stones)
        whitediff = len(self.move.white_stones)-len(self.start.white_stones)
        return blackdiff - whitediff
