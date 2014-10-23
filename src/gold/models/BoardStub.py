'''
Created on Oct 23, 2014

@author: JBlackmore
'''
from array import array

class BoardStub:
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.board_spaces = []
        for i in range(0, 18):
            row = array('c')
            for j in range(0, 18):
                row.append('0')
            self.board_spaces.append(row)
        self.board_spaces[2][3] = 'b'
        self.board_spaces[9][9] = 'w'
        self.board_spaces[9][10] = 'b'
        self.board_spaces[10][9] = 'w'
        
    def placeStone(self, row, col, color):
        self.board_spaces[row-1][col-1] = color[0]
        return self.board_spaces