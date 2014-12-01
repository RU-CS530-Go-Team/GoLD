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
    patchEx1 = PatchExtractor(self.start, self.start, self.movePosition, self.isblack)
    patchEx2 = PatchExtractor(self.start, self.move, self.movePosition, self.isblack)

    patchEx1.setPatchSize(4)
    patchEx2.setPatchSize(4)
    data41 = patchEx1.calculate_feature()
    data42 = patchEx2.calculate_feature()

    patchEx1.setPatchSize(5)
    patchEx2.setPatchSize(5)
    data51 = patchEx1.calculate_feature()
    data52 = patchEx2.calculate_feature()

    '''patchEx1.setPatchSize(6)
    patchEx2.setPatchSize(6)
    data61 = patchEx1.calculate_feature()
    data62 = patchEx2.calculate_feature()'''

    f = open('features/dictionary4.txt')
    dictionaryData = f.read()
    f.close()
    dictionary = pickle.loads(dictionaryData)
    data1 = dictionary.transform(data41)
    data2 = dictionary.transform(data42)
    data = data2 - data1
    features4 = np.amax(data, axis=0)

    f = open('features/dictionary5.txt')
    dictionaryData = f.read()
    f.close()
    dictionary = pickle.loads(dictionaryData)
    data1 = dictionary.transform(data51)
    data2 = dictionary.transform(data52)
    data = data2 - data1
    features5 = np.amax(data, axis=0)

    '''f = open('features/dictionary6.txt')
    dictionaryData = f.read()
    f.close()
    dictionary = pickle.loads(dictionaryData)
    data1 = dictionary.transform(data61)
    data2 = dictionary.transform(data62)
    data = data2 - data1
    features6 = np.amax(data, axis=0)'''

    return list(features4) + list(features5)# + list(features6)