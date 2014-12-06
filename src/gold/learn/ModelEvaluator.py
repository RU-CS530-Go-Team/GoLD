from gold.learn.Model import ModelBuilder

class ModelEvaluator():
  def __init__(self,outputFile,trainingFiles,testFiles,labels):
    fout=open(outputFile, 'w')
    fout.write("Model,Precision,Recall,F-Measure,Accuracy")
    for x in range(0,len(trainingFiles)):
      trFile = trainingFiles[x]
      teFile = testFiles[x]
      label = labels[x]
    fout.close()

  def testModel(trainingFile,testFile,numRuns,downsample,scale,pca,model):
    precision = 0
    recall = 0
    fmeasure = 0
    accuracy = 0
    runType = ""

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
      runType = runType + "AdaBoost

    for i in range(0,numRuns):
      temp = ModelBuilder([trainingFile],1)

      if scale == 1:
        runType = runType + "-scale"
        temp.buildScaler("scaler.txt")
        temp.scaleData()

      if downsample == 1:
        runType = runType + "-down"
        temp.downSample()

      if pca == 1:
        runType = runType + "-pca"
        temp.buildDimensionReducer("reducer.txt",False)
        temp.reduceDimensions()
      elif pca == 2:
        runType = runType + "-pcaW"
        temp.buildDimensionReducer("reducer.txt",True)
        temp.reduceDimensions()

      if model == 0:
        temp.buildModelLDA("model.txt")
      elif model == 1:
        temp.buildModelQDA("model.txt")
      elif model == 2:
        temp.buildModelLogReg("model.txt")
      elif model == 3:
        temp.buildModelNeighbors("model.txt")
      elif model == 4:
        temp.buildModelNB("model.txt")
      elif model == 5:
        temp.buildModelSVM("model.txt")
      elif model == 6:
        temp.buildModelRF("model.txt")
      elif model == 7:
        temp.buildModelAdaBoost("model.txt")



