from sklearn import svm
from sklearn import neighbors
from sklearn import ensemble
from sklearn import naive_bayes
from sklearn import preprocessing
from sklearn import decomposition
from sklearn import cross_validation
from sklearn import grid_search
from sklearn import lda
from sklearn import qda
from sklearn import linear_model
from gold.learn.FeatureSelector import FeatureSelector
from sklearn.feature_selection import RFE
import numpy as np
import pickle

class ModelBuilder():
  def __init__(self,inputFiles,classType=0):
    self.setData(inputFiles,classType)

  def setData(self,inputFiles,classType):
    self.instances = np.array([])
    self.classes = np.array([])
    for dataFile in inputFiles:
      data = np.loadtxt(open(dataFile,"rb"),delimiter=",",skiprows=1)
      #instancesTemp = data[:,:data.shape[1]-2]
      instancesTemp = data[:,:data.shape[1]-1]
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

  def buildFeatureSelector(self,outputFile,numFeatures):
    self.featureIndices = self.selectFeaturesFromSubsetRecursive(list(range(self.instances.shape[1])),numFeatures)
    featureSelectionData = pickle.dumps(self.featureIndices)
    f = open(outputFile,"w")
    f.write(featureSelectionData)
    f.close()

  def setFeaturesFromSelector(self,featureSelectorFile):
    f = open(featureSelectorFile)
    featureSelectionData = f.read()
    f.close()
    self.featureIndices = pickle.loads(featureSelectionData)

  def selectFeatures(self):
    self.instances = self.instances[:,self.featureIndices]

  def selectFeaturesFromSubsetRecursive(self,subset,numFeatures):
    model = svm.LinearSVC(class_weight='auto')
    rfe = RFE(model, numFeatures, verbose = 5)
    rfe = rfe.fit(self.instances[:,subset], self.classes)
    return rfe.get_support(indices=True)

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

  '''def buildModelSVM(self,outputFile,weights='auto'):
    classifier = svm.SVC(kernel='rbf',C=1.0,gamma=0.1,class_weight=weights)
    classifier.fit(self.instances, self.classes)
    modelData = pickle.dumps(classifier)
    f = open(outputFile,"w")
    f.write(modelData)
    f.close()'''

  def buildModelNeighbors(self,outputFile,maxSize=300,stepSize=10,folds=3,jobs=1):
    neighbor_range = np.arange(1,maxSize,stepSize)
    param_grid = dict(n_neighbors = neighbor_range)
    cv = cross_validation.StratifiedKFold(y=self.classes, n_folds=folds)
    grid = grid_search.GridSearchCV(neighbors.KNeighborsClassifier(), param_grid=param_grid, cv=cv, verbose=5, n_jobs=jobs)
    grid.fit(self.instances, self.classes)
    classifier = grid.best_estimator_
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

  def buildModelRF(self,outputFile,maxTrees=300,stepSize=10,folds=3,jobs=1):
    num_trees = np.arange(1,maxTrees,stepSize)
    param_grid = dict(n_estimators = num_trees)
    cv = cross_validation.StratifiedKFold(y=self.classes, n_folds=folds)
    grid = grid_search.GridSearchCV(ensemble.RandomForestClassifier(), param_grid=param_grid, cv=cv, verbose=5, n_jobs=jobs)
    grid.fit(self.instances, self.classes)
    classifier = grid.best_estimator_
    classifier.fit(self.instances, self.classes)
    modelData = pickle.dumps(classifier)
    f = open(outputFile,"w")
    f.write(modelData)
    f.close()

  def buildModelLogReg(self,outputFile,weights='auto'):
    classifier = linear_model.LogisticRegression(class_weight=weights)
    classifier.fit(self.instances, self.classes)
    modelData = pickle.dumps(classifier)
    f = open(outputFile,"w")
    f.write(modelData)
    f.close()

  def buildModelLDA(self,outputFile,priorProbs=[0.5,0.5]):
    classifier = qda.QDA(priors=priorProbs)
    classifier.fit(self.instances, self.classes)
    modelData = pickle.dumps(classifier)
    f = open(outputFile,"w")
    f.write(modelData)
    f.close()

  def buildModelQDA(self,outputFile,priorProbs=[0.5,0.5]):
    classifier = lda.LDA(priors=priorProbs)
    classifier.fit(self.instances, self.classes)
    modelData = pickle.dumps(classifier)
    f = open(outputFile,"w")
    f.write(modelData)
    f.close()

  def buildModelAdaBoost(self,outputFile):
    classifier = ensemble.AdaBoostClassifier()
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

    precision = float(truePositives) / (float(truePositives) + float(falsePositives) + 0.000001)

    recall = float(truePositives) / (float(truePositives) + float(falseNegatives) + 0.000001)

    fmeasure = 2*(precision*recall) / (precision + recall + 0.000001)

    return[precision, recall, fmeasure, accuracy]

class Model():
  # 0:SVM, 1:Anything else
  def __init__(self,modelFile,modelType):
    self.setModel(modelFile,modelType)

  # 0:SVM, 1:Anything else
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

  def setFeaturesFromSelector(self,featureSelectorFile):
    f = open(featureSelectorFile)
    featureSelectionData = f.read()
    f.close()
    self.featureIndices = pickle.loads(featureSelectionData)

  def selectFeatures(self):
    self.instances = self.instances[:,self.featureIndices]

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
