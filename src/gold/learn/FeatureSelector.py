from sklearn.ensemble import ExtraTreesClassifier
from sklearn import preprocessing
import numpy as np
from sklearn import svm
from sklearn.feature_selection import RFE

class FeatureSelector():
  def __init__(self,inputFiles,scaleDataFlag,downSampleFlag):
    self.setData(inputFiles)
    if scaleDataFlag:
      self.scaleData()
    if downSampleFlag:
      self.downSample()

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

  def downSample(self):
    numCorrect = np.count_nonzero(self.classes)
    numIncorrect = self.instances.shape[0] - numCorrect
    correctIndices = np.where(self.classes == 1)
    correctIndices = np.random.permutation(correctIndices[0][:])
    incorrectIndices = np.where(self.classes == 0)
    incorrectIndices = np.random.permutation(incorrectIndices[0][:])
    numSamples = min([numCorrect,numIncorrect])
    correctIndices = correctIndices[0:numSamples]
    incorrectIndices = incorrectIndices[0:numSamples]
    temp = self.instances[correctIndices,:]
    temp = np.concatenate((temp,self.instances[incorrectIndices,:]),axis=0)
    self.instances = temp
    temp = self.classes[correctIndices,:]
    temp = np.concatenate((temp,self.classes[incorrectIndices,:]),axis=0)
    self.classes = temp

  def selectFeaturesTreeBased(self,numFeatures):
    return self.selectFeaturesFromSubsetTreeBased(list(range(self.instances.shape[1])),numFeatures)

  def selectFeaturesFromSubsetTreeBased(self,subset,numFeatures):
    clf = ExtraTreesClassifier()
    clf.fit(self.instances[:,subset], self.classes)
    temp = clf.feature_importances_
    return np.argsort(-clf.feature_importances_)[:numFeatures]

  def selectFeaturesRecursive(self,numFeatures):
    return self.selectFeaturesFromSubsetRecursive(list(range(self.instances.shape[1])),numFeatures)

  def selectFeaturesFromSubsetRecursive(self,subset,numFeatures):
    model = svm.LinearSVC()
    rfe = RFE(model, numFeatures)
    rfe = rfe.fit(self.instances[:,subset], self.classes)
    # summarize the selection of the attributes
    print(rfe.get_support(indices=True))
    print(rfe.ranking_)
    return rfe.get_support(indices=True)
