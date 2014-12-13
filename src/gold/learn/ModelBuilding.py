import sys
import glob
sys.path.append("c:/Users/jblackmore/Documents/Development/Rutgers/GoLD/problems/resplit/")
from gold.learn.trainer import MoveTrainer
from gold.learn.Model import ModelBuilder
#from gold.learn.Model import Model

base = "c:/Users/jblackmore/Documents/Development/Rutgers/GoLD/problems/resplit/"
def extractFeatures():
    #Extract Features
    temp = MoveTrainer(["train/"])
    temp.train()
    temp = MoveTrainer(["dev/"])
    temp.train()

def buildModels():
    
    #Down-sample and use SVM
    print('Building SVM models...')
    temp = ModelBuilder([base+"trainfeaturesBtL.csv"])
    #temp.downSample()
    temp.buildModelSVM(base+"modelSVMBtL.txt")
    temp = ModelBuilder([base+"trainfeaturesWtK.csv"])
    #temp.downSample()
    temp.buildModelSVM(base+"modelSVMWtK.txt")
    
    #Down-sample, scale data, and use SVM
    print('Building scaled SVM models...')
    temp = ModelBuilder([base+"trainfeaturesBtL.csv"])
    #temp.downSample()
    temp.buildScaler(base+"trainfeaturesBtLScaler.txt")
    temp.scaleData()
    temp.buildModelSVM(base+"modelSVMsBtL.txt")

    temp = ModelBuilder([base+"trainfeaturesWtK.csv"])
    #temp.downSample()
    temp.buildScaler(base+"trainfeaturesWtKScaler.txt")
    temp.scaleData()
    temp.buildModelSVM(base+"modelSVMsWtK.txt")
    
    #Down-sample, scale data, apply PCA, and use SVM
    print('Building scaled PCA SVM models...')
    temp = ModelBuilder([base+"trainfeaturesBtL.csv"])
    #temp.downSample()
    temp.buildScaler(base+"trainfeaturesBtLScaler.txt")
    temp.scaleData()
    temp.buildDimensionReducer(base+"train/BtLReduce.txt",False)
    temp.reduceDimensions()
    temp.buildModelSVM(base+"modelSVMsrBtL.txt")

    temp = ModelBuilder([base+"trainfeaturesWtK.csv"])
    #temp.downSample()
    temp.buildScaler(base+"trainfeaturesWtKScaler.txt")
    temp.scaleData()
    temp.buildDimensionReducer(base+"train/WtKReduce.txt",False)
    temp.reduceDimensions()
    temp.buildModelSVM(base+"modelSVMsrWtK.txt")
    
    #Down-sample, apply PCA with whitening, and use SVM
    print('Building PCA with whitening SVM models...')
    temp = ModelBuilder([base+"trainfeaturesBtL.csv"])
    #temp.downSample()
    temp.buildDimensionReducer(base+"train/BtLReduceW.txt",True)
    temp.reduceDimensions()
    temp.buildModelSVM(base+"modelSVMsrwBtL.txt")

    temp = ModelBuilder([base+"trainfeaturesWtK.csv"])
    #temp.downSample()
    temp.buildDimensionReducer(base+"train/WtKReduceW.txt",True)
    temp.reduceDimensions()
    temp.buildModelSVM(base+"modelSVMsrwWtK.txt")
    
    #Use other models
    print('Building other models...')
    temp = ModelBuilder([base+"trainfeaturesBtL.csv"])
    #temp.downSample()
    #Weighted SVM: Class 0 Weight: 1, Class 1 Weight: 2
    temp.buildModelSVM(base+"modelSVMcwBtL.txt",weights={0:2,1:3})

    temp = ModelBuilder([base+"trainfeaturesWtK.csv"])
    #temp.downSample()
    #Weighted SVM: Class 0 Weight: 1, Class 1 Weight: 2
    temp.buildModelSVM(base+"modelSVMcwWtK.txt",weights={0:2,1:3})

    #5-Nearest Neighbors
    temp = ModelBuilder([base+"trainfeaturesBtL.csv"])
    temp.buildModelNeighbors(base+"modelNeighborsBtL.txt",5)
    temp = ModelBuilder([base+"trainfeaturesWtK.csv"])
    temp.buildModelNeighbors(base+"modelNeighborsWtK.txt",5)
    #Random forest of 10 trees
    temp = ModelBuilder([base+"trainfeaturesBtL.csv"])
    ##temp.downSample()
    temp.buildScaler(base+"trainfeaturesBtLScaler.txt")
    temp.scaleData()
    temp.buildModelRF(base+"modelRF10BtL.txt",10)
    temp.buildModelRF(base+"modelRF100BtL.txt",100)
    temp.buildModelNB(base+"modelNBBtL.txt")
    
    temp = ModelBuilder([base+"trainfeaturesWtK.csv"])
    ##temp.downSample()
    temp.buildScaler(base+"trainfeaturesWtKScaler.txt")
    temp.scaleData()
    temp.buildModelRF(base+"modelRF10WtK.txt",10)
    temp.buildModelRF(base+"modelRF100WtK.txt",100)
    temp.buildModelNB(base+"modelNBWtK.txt")
    print('Done! ')

def printStats(stats, blurb):
    precision = stats[0]
    recall = stats[1]
    fmeasure = stats[2]
    accuracy = stats[3]
    print('{}: p={:.3f} r={:.3f} f={:.3f} a={:.3f}'.format(blurb,precision,recall,fmeasure,accuracy))

def evaluateModels():
    temp = ModelBuilder([base+"devfeaturesBtL.csv"])
    stats = temp.evaluateModel(base+"modelSVMBtL.txt")
    printStats(stats, 'Unscaled SVM BtL')
    temp.setScaler(base+"trainfeaturesBtLScaler.txt")
    temp.scaleData()
    stats = temp.evaluateModel(base+"modelSVMsBtL.txt")
    printStats(stats, 'Scaled SVM BtL')

    stats = temp.evaluateModel(base+"modelNeighborsBtL.txt")
    printStats(stats, 'Scaled NN BtL')
    stats = temp.evaluateModel(base+"modelRF10BtL.txt")
    printStats(stats, 'Scaled RF10 BtL')
    stats = temp.evaluateModel(base+"modelRF100BtL.txt")
    printStats(stats, 'Scaled RF100 BtL')
    stats = temp.evaluateModel(base+"modelNBBtL.txt")

    temp.setDimensionReducer(base+"train/BtLReduce.txt")
    temp.reduceDimensions()
    stats = temp.evaluateModel(base+"modelSVMsrBtL.txt")
    printStats(stats, 'Scaled reduced SVM BtL')

    temp.setData([base+"devfeaturesBtL.csv"])
    temp.setScaler(base+"trainfeaturesBtLScaler.txt")
    temp.scaleData()
    temp.setDimensionReducer(base+"train/BtLReduceW.txt")
    temp.reduceDimensions()
    stats = temp.evaluateModel(base+"modelSVMsrwBtL.txt")
    printStats(stats, 'Scaled reduced PCA whitened SVM BtL')


    # --------------------------
    temp = ModelBuilder([base+"devfeaturesWtK.csv"])
    stats = temp.evaluateModel(base+"modelSVMWtK.txt")
    printStats(stats, 'Unscaled SVM WtK')
    
    temp.setScaler(base+"trainfeaturesWtKScaler.txt")
    temp.scaleData()
    stats = temp.evaluateModel(base+"modelSVMsWtK.txt")
    printStats(stats, 'Scaled SVM WtK')

    stats = temp.evaluateModel(base+"modelNeighborsWtK.txt")
    printStats(stats, 'Scaled NN WtK')
    stats = temp.evaluateModel(base+"modelRF10WtK.txt")
    printStats(stats, 'Scaled RF10 WtK')
    stats = temp.evaluateModel(base+"modelRF100WtK.txt")
    printStats(stats, 'Scaled RF100 WtK')
    stats = temp.evaluateModel(base+"modelNBWtK.txt")

    temp.setDimensionReducer(base+"train/WtKReduce.txt")
    temp.reduceDimensions()
    stats = temp.evaluateModel(base+"modelSVMsrWtK.txt")
    printStats(stats, 'Scaled reduced SVM WtK')

    temp.setData([base+"devfeaturesWtK.csv"])
    temp.setScaler(base+"trainfeaturesWtKScaler.txt")
    temp.scaleData()
    temp.setDimensionReducer(base+"train/WtKReduceW.txt")
    temp.reduceDimensions()
    stats = temp.evaluateModel(base+"modelSVMsrwWtK.txt")
    printStats(stats, 'Scaled reduced whitened SVM WtK')


buildModels()
evaluateModels()