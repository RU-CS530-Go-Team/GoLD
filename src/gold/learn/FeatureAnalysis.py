from gold.learn.Model import ModelBuilder
import time
import numpy as np
import csv

class FeatureAnalysis():

  labels = {1:'StoneCountFeature',2:'DiffLiberties',3:'DistanceFromCenterFeature',4:'numberLiveGroups',5:'LocalShapesFeature',6:'HuMomentsFeature',7:'SparseDictionaryFeature'}
  invariant = {1:[0,1,2,3,4,5],2:[9,10,11,12,13,14],3:[19],4:[20,21]}


  def __init__(self,outputFile,trainingFile,testFile):
    groupIndices = self.findGroupIndices(trainingFile[0])
    groupIndicesFeat = {}
    fout=open(outputFile, 'a')
    fout.write("Feature Set,Precision,Recall,F-Measure,Accuracy,AUROC,Number of Features")
    fout.write("\n")
    for i in range(1,11):
      if i == 1 or i == 2 or i == 4:
        subset = self.invariant[i]
        stats = self.runModelSubset(trainingFile,testFile,subset,False)
        string = self.labels[i] + "-inv," + ",".join([str(x) for x in stats])
        fout.write(string + "\n")
        print string
      if i == 9:
        subset = []
        for j in range(1,5):
          subset = subset + self.invariant[j]
        stats = self.runModelSubset(trainingFile,testFile,subset,False)
        string = "expert-inv," + ",".join([str(x) for x in stats])
        fout.write(string + "\n")
        print string
      if i == 10:
        subset = []
        for j in range(1,5):
          subset = subset + self.invariant[j]
        for j in range(5,8):
          subset = subset + groupIndices[self.labels[j]]
        stats = self.runModelSubset(trainingFile,testFile,subset,False)
        string = "all-inv," + ",".join([str(x) for x in stats])
        fout.write(string + "\n")
        print string

        subset = []
        for j in range(1,5):
          subset = subset + groupIndices[self.labels[j]]
        for j in range(6,8):
          subset = subset + groupIndices[self.labels[j]]
        stats = self.runModelSubset(trainingFile,testFile,subset,False)
        string = "all-noLoc," + ",".join([str(x) for x in stats])
        fout.write(string + "\n")
        print string

        subset = []
        for j in range(1,4):
          subset = subset + groupIndices[self.labels[j]]
        for j in range(5,8):
          subset = subset + groupIndices[self.labels[j]]
        stats = self.runModelSubset(trainingFile,testFile,subset,False)
        string = "all-noLive," + ",".join([str(x) for x in stats])
        fout.write(string + "\n")
        print string

        subset = []
        for j in range(1,4):
          subset = subset + groupIndices[self.labels[j]]
        for j in range(5,8):
          subset = subset + groupIndices[self.labels[j]]
        stats = self.runModelSubset(trainingFile,testFile,subset,False)
        string = "all-noLocLive," + ",".join([str(x) for x in stats])
        fout.write(string + "\n")
        print string

        '''if i < 8:
        subset = groupIndices[self.labels[i]]
        stats = self.runModelSubset(trainingFile,testFile,subset,False)
        string = self.labels[i] + "," + ",".join([str(x) for x in stats])
        fout.write(string + "\n")
        print string
        stats = self.runModelSubset(trainingFile,testFile,subset,True)
        string = self.labels[i] + "-feat," + ",".join([str(x) for x in stats])
        fout.write(string + "\n")
        print string
        selected = stats[6]
        adjustment = min(subset)
        for j in range(len(selected)):
          selected[j] = selected[j] + adjustment
        groupIndicesFeat[self.labels[i]] = selected
      if i == 8:
        subset = []
        for j in range(1,8):
          subset = subset + groupIndices[self.labels[j]]
        stats = self.runModelSubset(trainingFile,testFile,subset,False)
        string = "all," + ",".join([str(x) for x in stats])
        fout.write(string + "\n")
        print string
        stats = self.runModelSubset(trainingFile,testFile,subset,True)
        string = "all-feat-direct," + ",".join([str(x) for x in stats])
        fout.write(string + "\n")
        print string
        for j in range(1,8):
          subset = subset + groupIndicesFeat[self.labels[j]]
        stats = self.runModelSubset(trainingFile,testFile,subset,False)
        string = "all-feat-indirect," + ",".join([str(x) for x in stats])
        print string
        fout.write(string + "\n")
      if i == 9:
        subset = []
        for j in range(1,5):
          subset = subset + groupIndices[self.labels[j]]
        stats = self.runModelSubset(trainingFile,testFile,subset,False)
        string = "expert," + ",".join([str(x) for x in stats])
        fout.write(string + "\n")
        print string
        stats = self.runModelSubset(trainingFile,testFile,subset,True)
        string = "expert-feat-direct," + ",".join([str(x) for x in stats])
        fout.write(string + "\n")
        print string
        for j in range(1,5):
          subset = subset + groupIndicesFeat[self.labels[j]]
        stats = self.runModelSubset(trainingFile,testFile,subset,False)
        string = "expert-feat-indirect," + ",".join([str(x) for x in stats])
        print string
        fout.write(string + "\n")
      if i == 10:
        subset = []
        for j in range(6,8):
          subset = subset + groupIndices[self.labels[j]]
        stats = self.runModelSubset(trainingFile,testFile,subset,False)
        string = "general," + ",".join([str(x) for x in stats])
        fout.write(string + "\n")
        print string
        stats = self.runModelSubset(trainingFile,testFile,subset,True)
        string = "general-feat-direct," + ",".join([str(x) for x in stats])
        fout.write(string + "\n")
        print string
        for j in range(6,8):
          subset = subset + groupIndicesFeat[self.labels[j]]
        stats = self.runModelSubset(trainingFile,testFile,subset,False)
        string = "general-feat-indirect," + ",".join([str(x) for x in stats])
        print string
        fout.write(string + "\n")'''

    fout.close()


  def findGroupIndices(self,trainingFile):
    r = csv.reader(open(trainingFile))
    labelrow = r.next()
    groups = {}

    for i in range(1,8):
      groups[self.labels[i]] = []

    for i in range(len(labelrow)):
      for j in range(1,8):
        if labelrow[i].find(self.labels[j]) > -1:
          currentList = groups[self.labels[j]]
          currentList.append(i)
          groups[self.labels[j]] = currentList

    return groups

  def runModelSubset(self,trainingFile,testFile,subset,featureSelectionFlag,numRuns=3):
    stats = [0,0,0,0,0,0]
    features = set()
    for i in range(numRuns):
      temp = ModelBuilder(trainingFile,1)
      temp.setFeatures(subset)
      temp.downSample()
      temp.buildScaler("scalerXYZB.txt")
      temp.scaleData()
      featureIndices = subset
      if featureSelectionFlag:
        featureIndices = temp.buildFeatureSelectorAutomatic("selectorXYZB.txt",5)
        temp.selectFeatures()
      temp.buildModelRF("modelXYZB.txt",301,20,3,6)
      temp.setData(testFile,1)
      temp.setFeatures(subset)
      temp.setScaler("scalerXYZB.txt")
      temp.scaleData()
      if featureSelectionFlag:
        temp.setFeaturesFromSelector("selectorXYZB.txt")
        temp.selectFeatures()
      tempStats = temp.evaluateModel("modelXYZB.txt",plotROC=False)
      stats[0] = stats[0] + tempStats[0]
      stats[1] = stats[1] + tempStats[1]
      stats[2] = stats[2] + tempStats[2]
      stats[3] = stats[3] + tempStats[3]
      stats[4] = stats[4] + tempStats[4]
      stats[5] = stats[5] + len(featureIndices)
      features = features.union(set(featureIndices))
    stats[0] = stats[0] / numRuns
    stats[1] = stats[1] / numRuns
    stats[2] = stats[2] / numRuns
    stats[3] = stats[3] / numRuns
    stats[4] = stats[4] / numRuns
    stats[5] = stats[5] / float(numRuns)
    return stats + [list(features)]

