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
from sklearn.feature_selection import RFECV
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
import numpy as np
import pickle
import matplotlib.pyplot as plt

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
      classesTemp = None
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

  def buildFeatureSelectorAutomatic(self,outputFile,opttype = 5):
    model = svm.LinearSVC(class_weight='auto')

    if opttype == 1:
      rfecv = RFECV(estimator=model, step=1, cv=cross_validation.StratifiedKFold(self.classes, 2),
                scoring='roc_auc',verbose = 5)
      rfecv.fit(self.instances, self.classes)
      self.featureIndices = rfecv.get_support(indices=True)
      plt.figure()
      plt.xlabel("Number of features selected")
      plt.ylabel("Cross validation score (AUC)")
      plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
      plt.show()

    elif opttype == 2:
      rfecv = RFECV(estimator=model, step=1, cv=cross_validation.StratifiedKFold(self.classes, 2),
                scoring='f1',verbose = 5)
      rfecv.fit(self.instances, self.classes)
      self.featureIndices = rfecv.get_support(indices=True)
      plt.figure()
      plt.xlabel("Number of features selected")
      plt.ylabel("Cross validation score (f-measure)")
      plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
      plt.show()

    elif opttype == 3:
      rfecv = RFECV(estimator=model, step=1, cv=cross_validation.StratifiedKFold(self.classes, 2),
                scoring='accuracy',verbose = 5)
      rfecv.fit(self.instances, self.classes)
      self.featureIndices = rfecv.get_support(indices=True)
      plt.figure()
      plt.xlabel("Number of features selected")
      plt.ylabel("Cross validation score (accuracy)")
      plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
      plt.show()

    elif opttype == 4:
      rfecv = RFECV(estimator=model, step=1, cv=cross_validation.StratifiedKFold(self.classes, 2),
                scoring='recall',verbose = 5)
      rfecv.fit(self.instances, self.classes)
      self.featureIndices = rfecv.get_support(indices=True)
      plt.figure()
      plt.xlabel("Number of features selected")
      plt.ylabel("Cross validation score (recall)")
      plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
      plt.show()

    elif opttype == 5:
      rfecv = RFECV(estimator=model, step=1, cv=cross_validation.StratifiedKFold(self.classes, 2),
                scoring='average_precision',verbose = 5)
      rfecv.fit(self.instances, self.classes)
      self.featureIndices = rfecv.get_support(indices=True)
      #plt.figure()
      #plt.xlabel("Number of features selected")
      #plt.ylabel("Cross validation score (precision)")
      #plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
      #plt.show()

    featureSelectionData = pickle.dumps(self.featureIndices)
    f = open(outputFile,"w")
    f.write(featureSelectionData)
    f.close()
    return self.featureIndices

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
    temp = self.classes[correctIndices][:]
    temp = np.concatenate((temp,self.classes[incorrectIndices][:]),axis=0)
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

  def buildModelNeighbors(self,outputFile,maxSize=300,stepSize=10,folds=3,jobs=1,numNeighbors=None):
    classifier = None
    if numNeighbors == None:
      neighbor_range = np.arange(1,maxSize,stepSize)
      param_grid = dict(n_neighbors = neighbor_range)
      cv = cross_validation.StratifiedKFold(y=self.classes, n_folds=folds)
      grid = grid_search.GridSearchCV(neighbors.KNeighborsClassifier(), param_grid=param_grid, cv=cv, verbose=5, n_jobs=jobs)
      grid.fit(self.instances, self.classes)
      classifier = grid.best_estimator_
      classifier.fit(self.instances, self.classes)
    else:
      classifier = neighbors.KNeighborsClassifier(n_neighbors = numNeighbors)
      classifier.fit(self.instances, self.classes)
    modelData = pickle.dumps(classifier)
    f = open(outputFile,"w")
    f.write(modelData)
    f.close()
    return classifier.n_neighbors

  def buildModelNB(self,outputFile):
    classifier = naive_bayes.GaussianNB()
    classifier.fit(self.instances, self.classes)
    modelData = pickle.dumps(classifier)
    f = open(outputFile,"w")
    f.write(modelData)
    f.close()

  def buildModelRF(self,outputFile,maxTrees=300,stepSize=10,folds=3,jobs=1,numTrees=None):
    classifier = None
    if numTrees == None:
      num_trees = np.arange(1,maxTrees,stepSize)
      param_grid = dict(n_estimators = num_trees)
      cv = cross_validation.StratifiedKFold(y=self.classes, n_folds=folds)
      grid = grid_search.GridSearchCV(ensemble.RandomForestClassifier(), param_grid=param_grid, cv=cv, verbose=5, n_jobs=jobs, scoring='roc_auc')
      grid.fit(self.instances, self.classes)
      classifier = grid.best_estimator_
      classifier.fit(self.instances, self.classes)
    else:
      classifier = ensemble.RandomForestClassifier(n_estimators = numTrees)
      classifier.fit(self.instances, self.classes)
    modelData = pickle.dumps(classifier)
    f = open(outputFile,"w")
    f.write(modelData)
    f.close()
    return classifier.n_estimators

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

  def evaluateModel(self,modelFile,plotROC = False,modelType = 0):
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

    y_score = None

    if modelType == 0:
      y_score = classifier.predict_proba(self.instances[:][:])
    else:
      y_score = classifier.decision_function(self.instances[:][:])

    y_score = y_score[:,1]

    #Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(1):
        fpr[i], tpr[i], _ = roc_curve(self.classes[:], y_score[:])
        roc_auc[i] = auc(fpr[i], tpr[i])

    if plotROC:

      # Plot ROC curve
      plt.figure()
      for i in range(1):
          plt.plot(fpr[i], tpr[i], label='ROC curve of class {0} (area = {1:0.2f})'
                                         ''.format(i+1, roc_auc[i]))

      plt.plot([0, 1], [0, 1], 'k--')
      plt.xlim([0.0, 1.0])
      plt.ylim([0.0, 1.05])
      plt.xlabel('False Positive Rate')
      plt.ylabel('True Positive Rate')
      plt.title('ROC Curve: White to Kill')
      plt.legend(loc="lower right")
      plt.show()

    return[precision, recall, fmeasure, accuracy, roc_auc[0]]

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

  def setFeatures(self,instance,features):
    return instance[features]

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
