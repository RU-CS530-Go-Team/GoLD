from sklearn import svm
from sklearn import neighbors
from sklearn import ensemble
from sklearn import naive_bayes
from sklearn import preprocessing
from sklearn import decomposition
from sklearn import cross_validation
from sklearn import grid_search
import numpy as np
import pickle

class ModelBuilder():
  def __init__(self,inputFiles,classType):
    self.setData(inputFiles,classType)

  def setData(self,inputFiles,classType):
    self.instances = np.array([])
    self.classes = np.array([])
    for dataFile in inputFiles:
      data = np.loadtxt(open(dataFile,"rb"),delimiter=",",skiprows=1)
      instancesTemp = data[:,:data.shape[1]-2]
      if classType == 0:
        classesTemp = data[:,data.shape[1]-2]
      elif classType == 1:
        classesTemp = data[:,data.shape[1]-1]
      if self.instances.size == 0:
        self.instances = instancesTemp
        self.classes = classesTemp
      else:
        self.instances = np.concatenate((self.instances, instancesTemp), axis=0)
        self.classes = np.concatenate((self.classes, classesTemp), axis=0)

  def setFeatures(self,featureIndexList):
    self.instances = self.instances[:,featureIndexList]

  def buildScaler(self,outputFile):
    #Scale to zero mean, unit standard deviation
    self.scaler = preprocessing.StandardScaler().fit(self.instances)
    scalerData = pickle.dumps(self.scaler)
    f = open(outputFile,"w")
    f.write(scalerData)
    f.close()

  def buildDimensionReducer(self,outputFile,whitenFlag):
    self.pca = decomposition.PCA(n_components='mle',whiten=whitenFlag).fit(self.instances)
    pcaData = pickle.dumps(self.pca)
    f = open(outputFile,"w")
    f.write(pcaData)
    f.close()

  def setDimensionReducer(self,pcaFile):
    f = open(pcaFile)
    pcaData = f.read()
    f.close()
    self.pca = pickle.loads(pcaData)

  def setScaler(self,scalerFile):
    f = open(scalerFile)
    scalerData = f.read()
    f.close()
    self.scaler = pickle.loads(scalerData)

  def scaleData(self):
    self.instances = self.scaler.transform(self.instances)

  def reduceDimensions(self):
    self.instances = self.pca.transform(self.instances)

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

  def buildModelSVM(self,outputFile,weights='auto'):
    classifier = svm.LinearSVC(class_weight=weights)
    classifier.fit(self.instances, self.classes)
    modelData = pickle.dumps(classifier)
    f = open(outputFile,"w")
    f.write(modelData)
    f.close()

  '''def buildModelSVMRBF(self,outputFile):
    C_range = 10. ** np.arange(-3, 8)
    gamma_range = 10. ** np.arange(-5, 4)
    param_grid = dict(gamma=gamma_range, C=C_range)
    grid = grid_search.GridSearchCV(svm.SVC(), param_grid=param_grid, cv=cross_validation.StratifiedKFold(y=self.classes, n_folds=5))
    grid.fit(self.instances, self.classes)
    print("The best classifier is: ", grid.best_estimator_)
    #classifier = svm.SVC(class_weight=weights)
    #classifier.fit(self.instances, self.classes)
    #modelData = pickle.dumps(classifier)
    #f = open(outputFile,"w")
    #f.write(modelData)
    #f.close()'''

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
    accuracy = float(sum(correct)) / float(self.classes.shape[0])

    positiveIndices = np.where(self.classes == 1)
    negativeIndices = np.where(self.classes == 0)

    positivePredictiveIndices = np.where(predictions == 1)
    negativePredictiveIndices = np.where(predictions == 0)

    truePositives = len(np.intersect1d(positiveIndices[0][:],positivePredictiveIndices[0][:]))
    falseNegatives = len(np.intersect1d(positiveIndices[0][:],negativePredictiveIndices[0][:]))
    falsePositives = len(np.intersect1d(negativeIndices[0][:],positivePredictiveIndices[0][:]))

    precision = float(truePositives) / (float(truePositives) + float(falsePositives))

    recall = float(truePositives) / (float(truePositives) + float(falseNegatives))

    fmeasure = 2*(precision*recall) / (precision + recall)

    return[precision, recall, fmeasure, accuracy]

class Model():
  # 0:SVM, 1:kNN, 2:NB, 3:RF
  def __init__(self,modelFile,modelType):
    self.setModel(modelFile,modelType)

  # 0:SVM, 1:kNN, 2:NB, 3:RF
  def setModel(self,modelFile,modelType):
    f = open(modelFile)
    modelData = f.read()
    f.close()
    self.classifier = pickle.loads(modelData)
    self.modelType = modelType

  def setScaler(self,scalerFile):
    f = open(scalerFile)
    scalerData = f.read()
    f.close()
    self.scaler = pickle.loads(scalerData)

  def scale(self,instance):
    return self.scaler.transform(instance)

  def setDimensionReducer(self,pcaFile):
    f = open(pcaFile)
    pcaData = f.read()
    f.close()
    self.pca = pickle.loads(pcaData)

  def reduceDimensions(self):
    self.instances = self.pca.transform(self.instances)

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
