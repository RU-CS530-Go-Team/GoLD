'''
Created on Nov 17, 2014

@author: JBlackmore
'''

class Feature():
    '''
    classdocs
    '''
    

    def __init__(self, start, move, position, isblack, dataDir='../features/'):
        '''
        Constructor
        '''
        self.start = start
        self.move = move
        self.movePosition=position
        self.isblack = isblack
        self.dataDir = dataDir
        
    def name(self):
        return self.__class__.__name__
    
    def calculate_feature(self):
        raise NotImplementedError('Please implement calculate_feature()')