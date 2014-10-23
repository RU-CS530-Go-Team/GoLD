'''
Created on Oct 23, 2014

@author: JBlackmore
'''
from array import array

class BoardStub:
    def __init__(self):
        '''
        Constructor
        '''
        self.board_spaces = []
        for i in range(19):
            row = array('c')
            for j in range(19):
                row.append('0')
            self.board_spaces.append(row)

    '''
    row and col should be 0-based
    '''
    def placeStone(self, row, col, color):
        self.board_spaces[row][col] = color[0]
        return self.board_spaces