#TRY ROTATION
#TRY LARGER DICTIONARY SIZE
#CLUSTERING?
#FLIP MATRIX
'''
Created on Nov 29, 2014

@author: ZDaniels
'''
from Feature import Feature
from sklearn import decomposition
from sklearn.feature_extraction import image
import numpy as np
from PatchExtractor import PatchExtractor
import pickle

class SparseDictionaryFeature(Feature):

  def calculate_feature(self):
    data1 = PatchExtractor(self.start, self.start, self.movePosition, self.isblack).calculate_feature()
    data2 = PatchExtractor(self.start, self.move, self.movePosition, self.isblack).calculate_feature()
    f = open('features/dictionary.txt')
    dictionaryData = f.read()
    f.close()
    dictionary = pickle.loads(dictionaryData)
    data1 = dictionary.transform(data1)
    data2 = dictionary.transform(data2)
    data = data2 - data1
    features = np.amax(data, axis=0)
    return list(features)