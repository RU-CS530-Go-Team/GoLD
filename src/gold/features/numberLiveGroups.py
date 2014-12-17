'''
Created on Nov 28, 2014

@author: JGang
'''
from gold.models.life import determineLife
from gold.models.board import StoneGrouper
from Feature import Feature

class numberLiveGroups(Feature):
    '''
    classdocs
    '''
    def calculate_feature(self):
        first = len(determineLife(self.start, self.isblack))
        firstTotal = float(self.getNumGroups(self.start,self.isblack))
        second = len(determineLife(self.move, self.isblack))
        secondTotal = float(self.getNumGroups(self.start,self.isblack))
        return [second/(secondTotal+0.0001), (second/(secondTotal+0.0001)) - (first/(firstTotal+0.0001)), second, second - first]

    def getNumGroups(self,board,color):
      if color:
        stones = board.black_stones
        other = board.white_stones
      else:
        stones = board.white_stones
        other = board.black_stones
      initial_groups = [list(x) for x in StoneGrouper(stones).groups]
      return len(initial_groups)
