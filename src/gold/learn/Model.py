from sklearn import svm
from sklearn import neighbors
from sklearn import ensemble
from sklearn import naive_bayes
from sklearn import preprocessing
import numpy as np
import pickle

class ModelBuilder():
  def __init__(self,inputFiles):
    self.setData(inputFiles)

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
      print self.instances.size
  def buildModelSVM(self,outputFile):
    classifier = svm.LinearSVC()
    classifier.fit(self.instances, self.classes)
    modelData = pickle.dumps(classifier)
    f = open(outputFile,"w")
    f.write(modelData)
    f.close()

  def buildScaler(self,outputFile):
    #Scale to zero mean, unit standard deviation
    self.scaler = preprocessing.StandardScaler().fit(self.instances)
    scalerData = pickle.dumps(scaler)
    f = open(outputFile,"w")
    f.write(scalerData)
    f.close()

  def setScaler(self,scalerFile):
    f = open(scalerFile)
    scalerData = f.read()
    self.scaler = pickle.loads(scalerData)

  def scaleData():
    self.instances = self.scaler.transform(self.instances)

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

  def setScaler(self,scalerFile):
    f = open(scalerFile)
    scalerData = f.read()
    self.scaler = pickle.loads(scalerData)

  def scale(self,instance):
    return self.scaler.transform(instance)

  def classify(self,instance):
    predictions = self.classifier.predict(instance)
    return predictions[0]

  def getScoreCorrect(self,instance):
    score = None
    #SVM scores are the signed distance from decision boundary, >0 ==> class 1, <0 ==> class 0
    if self.modelType == 0:
      score = self.classifier.decision_function(instance)
      score = score[0]
    else:
      score = self.classifier.predict_proba(instance)
      score = score[0][1]
    return score
