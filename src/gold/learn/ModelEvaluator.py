from gold.learn.Model import ModelBuilder
import time

class ModelEvaluator():
  def __init__(self,outputFile,trainingFiles,testFiles,labels):
    start = time.clock()
    fout=open(outputFile, 'w')
    fout.write("Model,Precision,Recall,F-Measure,Accuracy")
    fout.write("\n")
    for x in range(0,len(trainingFiles)):
      trainingFile = trainingFiles[x]
      testFile = testFiles[x]
      label = labels[x]
      for model in range(0,8):
        for downsample in range(0,2):
          for scale in range(0,2):
            for pca in range(0,3):
              info = self.testModel(trainingFile,testFile,3,downsample,scale,pca,model,label)
              fout.write(info)
              fout.write("\n")

    fout.close()
    end = time.clock()
    intvl = end - start
    print('Evaluation took %.03f seconds' %intvl)

  def testModel(self,trainingFile,testFile,numRuns,downsample,scale,pca,model,label):
    precision = 0
    recall = 0
    fmeasure = 0
    accuracy = 0
    runType = label

    if model == 0:
      runType = runType + "LDA"
    elif model == 1:
      runType = runType + "QDA"
    elif model == 2:
      runType = runType + "LogReg"
    elif model == 3:
      runType = runType + "kNN"
    elif model == 4:
      runType = runType + "NaiveBayes"
    elif model == 5:
      runType = runType + "LinearSVM"
    elif model == 6:
      runType = runType + "RandForest"
    elif model == 7:
      runType = runType + "AdaBoost"

    if scale == 1:
      runType = runType + "-scale"

    if downsample == 1:
      runType = runType + "-down"

    if pca == 1:
      runType = runType + "-pca"
    elif pca == 2:
      runType = runType + "-pcaW"

    featureSelector = ""
    if label == "BtL":
      featureSelector = "learn/BtLFeatureSelector.txt"
    elif label == "WtK":
      featureSelector = "learn/WtKFeatureSelector.txt"

    for i in range(0,numRuns):
      temp = ModelBuilder([trainingFile],1)

      if scale == 1:
        temp.buildScaler("scaler.txt")
        temp.scaleData()

      if downsample == 1:
        temp.downSample()

      temp.setFeaturesFromSelector(featureSelector)
      temp.selectFeatures()

      if pca == 1:
        try:
          temp.buildDimensionReducer("reducer.txt",False)
          temp.reduceDimensions()
        except Exception as error:
          print error
          numRuns = numRuns - 1
          continue
          runType = runType + "-pcaErr"
          pca = 0
      elif pca == 2:
        try:
          temp.buildDimensionReducer("reducer.txt",True)
          temp.reduceDimensions()
        except Exception as error:
          print error
          numRuns = numRuns - 1
          continue
          runType = runType + "-pcaWErr"
          pca = 0

      if model == 0:
        temp.buildModelLDA("model.txt")
      elif model == 1:
        temp.buildModelQDA("model.txt")
      elif model == 2:
        temp.buildModelLogReg("model.txt")
      elif model == 3:
        if downsample == 1:
          temp.buildModelNeighbors("model.txt",202,20,3,6)
        else:
          temp.buildModelNeighbors("model.txt",102,25,3,6)
      elif model == 4:
        temp.buildModelNB("model.txt")
      elif model == 5:
        temp.buildModelSVM("model.txt")
      elif model == 6:
        temp.buildModelRF("model.txt",202,20,3,6)
      elif model == 7:
        temp.buildModelAdaBoost("model.txt")

      temp.setData([testFile],1)

      if scale == 1:
        temp.setScaler("scaler.txt")
        temp.scaleData()

      temp.setFeaturesFromSelector(featureSelector)
      temp.selectFeatures()

      if pca == 1 or pca == 2:
        temp.setDimensionReducer("reducer.txt")
        temp.reduceDimensions()

      stats = temp.evaluateModel("model.txt")

      precision = precision + stats[0]
      recall = recall + stats[1]
      fmeasure = fmeasure + stats[2]
      accuracy = accuracy + stats[3]

    precision = float(precision) / float(numRuns + 0.000001)
    recall = float(recall) / float(numRuns + 0.000001)
    fmeasure = float(fmeasure) / float(numRuns + 0.000001)
    accuracy = float(accuracy) / float(numRuns + 0.000001)
    print runType + "," + str(precision) + "," + str(recall) + "," + str(fmeasure) + "," + str(accuracy)
    return runType + "," + str(precision) + "," + str(recall) + "," + str(fmeasure) + "," + str(accuracy)



