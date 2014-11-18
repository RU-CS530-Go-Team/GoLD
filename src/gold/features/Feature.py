'''
Created on Nov 17, 2014

@author: JBlackmore
'''

class Feature():
    '''
    classdocs
    '''
    

    def __init__(self, start, move):
        '''
        Constructor
        '''
        self.start = start
        self.move = move
    
    def calculate_feature(self):
        raise NotImplementedError('Please implement calculate_feature()')