from sklearn import svm
from sklearn import neighbors
from sklearn import ensemble
from sklearn import naive_bayes
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

  def buildModelNeighbors(self,outputFile,numNeighbors):
    classifier = neighbors.KNeighborsClassifier(numNeighbors)
    classifier.fit(self.instances, self.classes)
    modelData = pickle.dumps(classifier)
    f = open(outputFile,"w")
    f.write(modelData)
    f.close()

  def buildModelNB(self,outputFile):
    classifier = naive_bayes.GaussianNB()
    classifier.fit(self.instances, self.classes)
    modelData = pickle.dumps(classifier)
    f = open(outputFile,"w")
    f.write(modelData)
    f.close()

  def buildModelRF(self,outputFile,numTrees):
    classifier = ensemble.RandomForestClassifier(numTrees)
    classifier.fit(self.instances, self.classes)
    modelData = pickle.dumps(classifier)
    f = open(outputFile,"w")
    f.write(modelData)
    f.close()

  def evaluateModel(self,modelFile):
    f = open(modelFile)
    modelData = f.read()
    classifier = pickle.loads(modelData)
    predictions = classifier.predict(self.instances)
    correct = (predictions == self.classes)
    #returns percent correctly classified
    return float(sum(correct)) / float(self.classes.shape[0])

class Model():
  # 0:SVM, 1:kNN, 2:NB, 3:RF
  def __init__(self,modelFile,modelType):
    self.setModel(modelFile,modelType)

  # 0:SVM, 1:kNN, 2:NB, 3:RF
  def setModel(self,modelFile,modelType):
    f = open(modelFile)
    modelData = f.read()
    self.classifier = pickle.loads(modelData)
    self.modelType = modelType

  def classify(self,instance):
    predictions = self.classifier.predict(instance)
    return predictions[0]

  def getScoreCorrect(self,instance):
    score = None
    #SVM scores are the signed distance from decision boundary, >0 ==> class 1, <0 ==> class 0
    if self.modelType == 1:
      score = self.classifier.decision_function(instance)
      score = score[0]
    else:
      score = self.classifier.predict_proba(instance)
      score = score[0][1]
    return score