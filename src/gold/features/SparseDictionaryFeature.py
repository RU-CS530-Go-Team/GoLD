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
    data = PatchExtractor(self.start, self.move, self.movePosition, self.isblack).calculate_feature()
    f = open('features/dictionary.txt')
    dictionaryData = f.read()
    f.close()
    dictionary = pickle.loads(dictionaryData)
    data = dictionary.transform(data)
    features = np.average(data, axis=0)
    return list(features)