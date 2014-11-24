from sklearn import svm
import numpy as np
import pickle

class ModelBuilder():
  def __init__(self,inputFile):
    self.setData(inputFile)

  def setData(self,inputFile):
    self.dataFile = inputFile
    self.data = np.loadtxt(open(self.dataFile,"rb"),delimiter=",",skiprows=1)
    self.instances = self.data[:,:self.data.shape[1]-1]
    self.classes = self.data[:,self.data.shape[1]-1]

  def buildModelSVM(self,outputFile):
    classifier = svm.LinearSVC()
    classifier.fit(self.instances, self.classes)
    modelData = pickle.dumps(classifier)
    f = open(outputFile,"w")
    f.write(modelData)
    f.close()

  def evaluateModelSVM(self,modelFile):
    f = open(modelFile)
    modelData = f.read()
    classifier = pickle.loads(modelData)
    predictions = classifier.predict(self.instances)
    correct = (predictions == self.classes)
    #returns percent correctly classified
    return float(sum(correct)) / float(self.classes.shape[0])
