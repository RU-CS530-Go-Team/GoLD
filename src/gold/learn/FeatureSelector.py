from sklearn.ensemble import ExtraTreesClassifier
from sklearn import preprocessing
import numpy as np
import pickle

class FeatureSelector():
  def __init__(self,inputFiles,scaleDataFlag,numFeatures):
    self.setData(inputFiles)
    if scaleDataFlag:
      self.scaleData()
    return self.selectFeatures(numFeatures)

  def setData(self,inputFiles):
    self.instances = np.array([])
    self.classes = np.array([])
    for dataFile in inputFiles:
      data = np.loadtxt(open(dataFile,"rb"),delimiter=",",skiprows=1)
      instancesTemp = data[:,:data.shape[1]-1]
      classesTemp = data[:,data.shape[1]-1]
      if self.instances.size == 0:
        self.instances = instancesTemp
        self.classes = classesTemp
      else:
        self.instances = np.concatenate((self.instances, instancesTemp), axis=0)
        self.classes = np.concatenate((self.classes, classesTemp), axis=0)

  def scaleData(self):
    #Scale to zero mean, unit standard deviation
    self.scaler = preprocessing.StandardScaler().fit(self.instances)
    self.instances = self.scaler.transform(self.instances)

  def selectFeatures(self,numFeatures):
    clf = ExtraTreesClassifier()
    clf.fit(self.instances, self.classes)
    return np.argsort(-clf.feature_importances_)[:numFeatures]