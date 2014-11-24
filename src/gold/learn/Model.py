from sklearn import svm
import numpy as np
import pickle

class ModelBuilder():
  def __init__(self,inputFile):
    self.trainingFile = inputFile
    self.trainingData = np.loadtxt(open(self.trainingFile,"rb"),delimiter=",",skiprows=1)
    self.instances = self.trainingData[:,:self.trainingData.shape[1]-1]
    self.classes = self.trainingData[:,self.trainingData.shape[1]-1]

  def buildModelSVM(self,outputFile):
    clf = svm.LinearSVC()
    clf.fit(self.instances, self.classes)
    s = pickle.dumps(clf)
    f = open(outputFile,"w")
    f.write(s)
    f.close()