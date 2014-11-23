'''
Created on Nov 22, 2014

@author: JBlackmore
'''

from gold.features.Feature import Feature

class ColorFeature(Feature):
    '''
    classdocs
    '''

    def calculate_feature(self):
        if self.isblack:
            return 1
        return 0
        