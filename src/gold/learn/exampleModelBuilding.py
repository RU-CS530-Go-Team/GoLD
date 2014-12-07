import sys
sys.path.append("/Users/zacharydaniels/Documents/GoLD/src/")
from gold.learn.trainer import MoveTrainer
from gold.learn.Model import ModelBuilder
from gold.learn.Model import Model

#Extract Features
temp = MoveTrainer(["extraneous/games/train/"])
temp.train()
temp = MoveTrainer(["extraneous/games/dev/"])
temp.train()

#0: Good move or bad move, 1: terminal solution state or not
classType = 0

#SVM
temp = ModelBuilder(["extraneous/games/train/featuresBtL.csv"],classType)
temp.buildModelSVM("extraneous/games/train/modelSVMBtL.txt", weights='auto')
#temp.setData(["extraneous/games/dev/featuresBtL.csv"],classType)
temp.evaluateModel("extraneous/games/train/modelSVMBtL.txt")
temp = ModelBuilder(["extraneous/games/train/featuresWtK.csv"],classType)
temp.buildModelSVM("extraneous/games/train/modelSVMWtK.txt")
#temp.setData(["extraneous/games/dev/featuresWtK.csv"],classType)
temp.evaluateModel("extraneous/games/train/modelSVMWtK.txt")

#Scale data and use SVM
temp = ModelBuilder(["extraneous/games/train/featuresBtL.csv"],classType)
temp.buildScaler("extraneous/games/train/featuresBtLScaler.txt")
temp.scaleData()
temp.buildModelSVM("extraneous/games/train/modelSVM.txt")
temp.setData(["extraneous/games/dev/featuresBtL.csv"],classType)
temp.setScaler("extraneous/games/train/featuresBtLScaler.txt")
temp.scaleData()
temp.evaluateModel("extraneous/games/train/modelSVM.txt")
temp = ModelBuilder(["extraneous/games/train/featuresWtK.csv"],classType)
temp.buildScaler("extraneous/games/train/featuresWtKScaler.txt")
temp.scaleData()
temp.buildModelSVM("extraneous/games/train/modelSVM.txt")
temp.setData(["extraneous/games/dev/featuresWtK.csv"],classType)
temp.setScaler("extraneous/games/train/featuresWtKScaler.txt")
temp.scaleData()
temp.evaluateModel("extraneous/games/train/modelSVM.txt")

#Scale data, apply PCA, and use SVM
temp = ModelBuilder(["extraneous/games/train/featuresBtL.csv"],classType)
temp.buildScaler("extraneous/games/train/featuresBtLScaler.txt")
temp.scaleData()
temp.buildDimensionReducer("extraneous/games/train/BtLReduce.txt",False)
temp.reduceDimensions()
temp.buildModelSVM("extraneous/games/train/modelSVM.txt")
temp.setData(["extraneous/games/dev/featuresBtL.csv"],classType)
temp.setScaler("extraneous/games/train/featuresBtLScaler.txt")
temp.scaleData()
temp.setDimensionReducer("extraneous/games/train/BtLReduce.txt")
temp.reduceDimensions()
temp.evaluateModel("extraneous/games/train/modelSVM.txt")
temp = ModelBuilder(["extraneous/games/train/featuresWtK.csv"],classType)
temp.buildScaler("extraneous/games/train/featuresWtKScaler.txt")
temp.scaleData()
temp.buildDimensionReducer("extraneous/games/train/WtKReduce.txt",False)
temp.reduceDimensions()
temp.buildModelSVM("extraneous/games/train/modelSVM.txt")
temp.setData(["extraneous/games/dev/featuresWtK.csv"],classType)
temp.setScaler("extraneous/games/train/featuresWtKScaler.txt")
temp.scaleData()
temp.setDimensionReducer("extraneous/games/train/WtKReduce.txt")
temp.reduceDimensions()
temp.evaluateModel("extraneous/games/train/modelSVM.txt")

#Apply PCA with whitening and use SVM
temp = ModelBuilder(["extraneous/games/train/featuresBtL.csv"],classType)
temp.buildDimensionReducer("extraneous/games/train/BtLReduce.txt",True)
temp.reduceDimensions()
temp.buildModelSVM("extraneous/games/train/modelSVM.txt")
temp.setData(["extraneous/games/dev/featuresBtL.csv"],classType)
temp.setDimensionReducer("extraneous/games/train/BtLReduce.txt")
temp.reduceDimensions()
temp.evaluateModel("extraneous/games/train/modelSVM.txt")
temp = ModelBuilder(["extraneous/games/train/featuresWtK.csv"],classType)
temp.buildDimensionReducer("extraneous/games/train/WtKReduce.txt",True)
temp.reduceDimensions()
temp.buildModelSVM("extraneous/games/train/modelSVM.txt")
temp.setData(["extraneous/games/dev/featuresWtK.csv"],classType)
temp.setDimensionReducer("extraneous/games/train/WtKReduce.txt")
temp.reduceDimensions()
temp.evaluateModel("extraneous/games/train/modelSVM.txt")

#Use other models
temp = ModelBuilder(["extraneous/games/train/featuresBtL.csv"],classType)
temp.downSample()
#Weighted SVM: Class 0 Weight: 1, Class 1 Weight: 2
temp.buildModelSVM("extraneous/games/train/modelSVM.txt",weights={0:2,1:3})
#5-Nearest Neighbors
temp.buildModelNeighbors("extraneous/games/train/modelNeighbors.txt",5)
#Random forest of 10 trees
temp.buildModelRF("extraneous/games/train/modelRF.txt",10)
temp.buildModelNB("extraneous/games/train/modelNB.txt")
temp.setData(["extraneous/games/dev/featuresBtL.csv"],classType)
temp.evaluateModel("extraneous/games/train/modelSVM.txt")
temp.evaluateModel("extraneous/games/train/modelNeighbors.txt")
temp.evaluateModel("extraneous/games/train/modelRF.txt")
temp.evaluateModel("extraneous/games/train/modelNB.txt")

temp = ModelBuilder(["extraneous/games/train/featuresWtK.csv"],classType)
temp.downSample()
#Weighted SVM: Class 0 Weight: 1, Class 1 Weight: 2
temp.buildModelSVM("extraneous/games/train/modelSVM.txt",weights={0:2,1:3})
#5-Nearest Neighbors
temp.buildModelNeighbors("extraneous/games/train/modelNeighbors.txt",5)
#Random forest of 10 trees
temp.buildModelRF("extraneous/games/train/modelRF.txt",10)
temp.buildModelNB("extraneous/games/train/modelNB.txt")
temp.setData(["extraneous/games/dev/featuresWtK.csv"],classType)
temp.evaluateModel("extraneous/games/train/modelSVM.txt")
temp.evaluateModel("extraneous/games/train/modelNeighbors.txt")
temp.evaluateModel("extraneous/games/train/modelRF.txt")
temp.evaluateModel("extraneous/games/train/modelNB.txt")
