'''
Created on Nov 28, 2014

@author: JGang
'''
from gold.extraneous.life import determineLife
from Feature import Feature

class numberLiveGroups(Feature):
    '''
    classdocs
    '''
    def calculate_feature(self):
        first = len(determineLife(self.start, self.isblack))
        second = len(determineLife(self.move, self.isblack))
        return second - first