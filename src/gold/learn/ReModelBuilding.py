import sys
import glob
import time
sys.path.append("c:/Users/jblackmore/Documents/Development/Rutgers/GoLD/problems/resplit/newmodels")
from gold.features.trainer import MoveTrainer
from gold.learn.Model import ModelBuilder
#from gold.learn.Model import Model

base = "c:/Users/jblackmore/Documents/Development/Rutgers/GoLD/problems/resplit/models/"
def extractFeatures():
    #Extract Features
    temp = MoveTrainer(["train/"])
    temp.train()
    temp = MoveTrainer(["dev/"])
    temp.train()

def buildModels():
    start = time.clock()
    istart = start
    #Down-sample and use SVM
    print('Building SVM models...')
    temp = ModelBuilder([base+"trainfeaturesBtL.csv"],1)
    print('Loaded model builder {:.3f} sec...'.format(time.clock()-start))
    #temp.downSample()
    temp.buildModelSVM(base+"modelSVMBtL.txt")
    print('BtL model built {:.3f} sec...'.format(time.clock()-istart))
    istart = time.clock()
    temp = ModelBuilder([base+"trainfeaturesWtK.csv"],1)
    #temp.downSample()
    temp.buildModelSVM(base+"modelSVMWtK.txt")
    print('WtKmodel built {:.3f} sec...'.format(time.clock()-istart))
    
    #Down-sample, scale data, and use SVM
    print('Building scaled SVM models...')
    temp = ModelBuilder([base+"trainfeaturesBtL.csv"],1)
    #temp.downSample()
    temp.buildScaler(base+"trainfeaturesBtLScaler.txt")
    temp.scaleData()
    temp.buildModelSVM(base+"modelSVMsBtL.txt")

    temp = ModelBuilder([base+"trainfeaturesWtK.csv"],1)
    #temp.downSample()
    temp.buildScaler(base+"trainfeaturesWtKScaler.txt")
    temp.scaleData()
    temp.buildModelSVM(base+"modelSVMsWtK.txt")
    
    #Down-sample, scale data, apply PCA, and use SVM
    print('Building scaled PCA SVM models...')
    temp = ModelBuilder([base+"trainfeaturesBtL.csv"],1)
    #temp.downSample()
    temp.buildScaler(base+"trainfeaturesBtLScaler.txt")
    temp.scaleData()
    temp.buildDimensionReducer(base+"BtLReduce.txt",False)
    temp.reduceDimensions()
    temp.buildModelSVM(base+"modelSVMsrBtL.txt")

    temp = ModelBuilder([base+"trainfeaturesWtK.csv"],1)
    #temp.downSample()
    temp.buildScaler(base+"trainfeaturesWtKScaler.txt")
    temp.scaleData()
    temp.buildDimensionReducer(base+"WtKReduce.txt",False)
    temp.reduceDimensions()
    temp.buildModelSVM(base+"modelSVMsrWtK.txt")
    
    #Down-sample, apply PCA with whitening, and use SVM
    print('Building PCA with whitening SVM models...')
    temp = ModelBuilder([base+"trainfeaturesBtL.csv"],1)
    temp.downSample()
    temp.buildDimensionReducer(base+"BtLReduceW.txt",True)
    temp.reduceDimensions()
    temp.buildModelSVM(base+"modelSVMsrwBtL.txt")

    temp = ModelBuilder([base+"trainfeaturesWtK.csv"],1)
    temp.downSample()
    temp.buildDimensionReducer(base+"WtKReduceW.txt",True)
    temp.reduceDimensions()
    temp.buildModelSVM(base+"modelSVMsrwWtK.txt")
    
    #Use other models
    print('Building other models...')
    temp = ModelBuilder([base+"trainfeaturesBtL.csv"],1)
    temp.downSample()
    #Weighted SVM: Class 0 Weight: 1, Class 1 Weight: 2
    temp.buildModelSVM(base+"modelSVMcwBtL.txt",weights={0:2,1:3})
    #5-Nearest Neighbors
    temp.buildModelNeighbors(base+"modelNeighborsBtL.txt",5)
    #Random forest of 10 trees
    temp.buildModelRF(base+"modelRF10BtL.txt",10)
    temp.buildModelRF(base+"modelRF100BtL.txt",100)
    temp.buildModelNB(base+"modelNBBtL.txt")
    
    temp = ModelBuilder([base+"trainfeaturesWtK.csv"],1)
    temp.downSample()
    #Weighted SVM: Class 0 Weight: 1, Class 1 Weight: 2
    temp.buildModelSVM(base+"modelSVMcwWtK.txt",weights={0:2,1:3})
    #5-Nearest Neighbors
    temp.buildModelNeighbors(base+"modelNeighborsWtK.txt",5)
    #Random forest of 10 trees
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

def evaluateBtL():
    evaluateModel('BtL')
    '''
    temp = ModelBuilder([base+"devfeaturesBtL.csv"],1)
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
    printStats(stats, 'Scaled NB BtL')

    temp.setDimensionReducer(base+"BtLReduce.txt")
    temp.reduceDimensions()
    stats = temp.evaluateModel(base+"modelSVMsrBtL.txt")
    printStats(stats, 'Scaled reduced SVM BtL')

    #temp.setData([base+"devfeaturesBtL.csv"])
    temp = ModelBuilder([base+"devfeaturesBtL.csv"],1)
    temp.setScaler(base+"trainfeaturesBtLScaler.txt")
    temp.scaleData()
    temp.setDimensionReducer(base+"BtLReduceW.txt")
    temp.reduceDimensions()
    stats = temp.evaluateModel(base+"modelSVMsrwBtL.txt")
    printStats(stats, 'Scaled reduced PCA whitened SVM BtL')
    '''
def evaluateModel(modelType):
    temp = ModelBuilder([base+"devfeatures"+modelType+".csv"],1)
    stats = temp.evaluateModel(base+"modelSVM"+modelType+".txt")
    printStats(stats, 'Unscaled SVM '+modelType)
    stats = temp.evaluateModel(base+"modelSVMcw"+modelType+".txt")
    printStats(stats, 'Unscaled weighted SVM '+modelType)
    stats = temp.evaluateModel(base+"modelNeighbors"+modelType+".txt")
    printStats(stats, 'Unscaled NN '+modelType)
    stats = temp.evaluateModel(base+"modelRF10"+modelType+".txt")
    printStats(stats, 'Unscaled RF10 '+modelType)
    stats = temp.evaluateModel(base+"modelRF100"+modelType+".txt")
    printStats(stats, 'Unscaled RF100 '+modelType)
    stats = temp.evaluateModel(base+"modelNB"+modelType+".txt")
    printStats(stats, 'Unscaled NB '+modelType)

    temp.setScaler(base+"trainfeaturesWtKScaler.txt")
    temp.scaleData()
    stats = temp.evaluateModel(base+"modelSVMs"+modelType+".txt")
    printStats(stats, 'Scaled SVM '+modelType)

    temp.setDimensionReducer(base+"WtKReduce.txt")
    temp.reduceDimensions()
    stats = temp.evaluateModel(base+"modelSVMsr"+modelType+".txt")
    printStats(stats, 'Scaled reduced SVM '+modelType)

    temp = ModelBuilder([base+"devfeatures"+modelType+".csv"],1)
    temp.setScaler(base+"trainfeaturesWtKScaler.txt")
    temp.scaleData()
    temp.setDimensionReducer(base+"WtKReduceW.txt")
    temp.reduceDimensions()
    stats = temp.evaluateModel(base+"modelSVMsrw"+modelType+".txt")
    printStats(stats, 'Scaled reduced whitened SVM '+modelType)
    
    # --------------------------
def evaluateWtK():
    evaluateModel("WtK")
    '''
    temp = ModelBuilder([base+"devfeaturesWtK.csv"],1)
    stats = temp.evaluateModel(base+"modelSVMWtK.txt")
    printStats(stats, 'Unscaled SVM WtK')
    stats = temp.evaluateModel(base+"modelSVMcwWtK.txt")
    printStats(stats, 'Unscaled weighted SVM WtK')
    stats = temp.evaluateModel(base+"modelNeighborsWtK.txt")
    printStats(stats, 'Unscaled NN WtK')
    stats = temp.evaluateModel(base+"modelRF10WtK.txt")
    printStats(stats, 'Unscaled RF10 WtK')
    stats = temp.evaluateModel(base+"modelRF100WtK.txt")
    printStats(stats, 'Unscaled RF100 WtK')
    stats = temp.evaluateModel(base+"modelNBWtK.txt")
    printStats(stats, 'Unscaled NB WtK')

    temp.setScaler(base+"trainfeaturesWtKScaler.txt")
    temp.scaleData()
    stats = temp.evaluateModel(base+"modelSVMsWtK.txt")
    printStats(stats, 'Scaled SVM WtK')

    temp.setDimensionReducer(base+"WtKReduce.txt")
    temp.reduceDimensions()
    stats = temp.evaluateModel(base+"modelSVMsrWtK.txt")
    printStats(stats, 'Scaled reduced SVM WtK')

    temp = ModelBuilder([base+"devfeaturesWtK.csv"],1)
    temp.setScaler(base+"trainfeaturesWtKScaler.txt")
    temp.scaleData()
    temp.setDimensionReducer(base+"WtKReduceW.txt")
    temp.reduceDimensions()
    stats = temp.evaluateModel(base+"modelSVMsrwWtK.txt")
    printStats(stats, 'Scaled reduced whitened SVM WtK')
    '''
def buildTermModelsN(probtype, downSample=False):
    start = time.clock()
    istart = start
    if probtype == 1:
        suffix = 'BtL_T'
        ptdesc = 'BtL'
    else:
        suffix = 'WtK_T'
        ptdesc = 'WtK'
    #Down-sample and use SVM
    print('Building SVM models for {}...'.format(suffix))
    temp = ModelBuilder([base+"trainfeaturesBtL_T.csv".format(suffix)],1)
    print('Loaded model builder {:.3f} sec...'.format(time.clock()-start))
    if downSample:
        temp.downSample()
    temp.buildModelSVM(base+"modelSVMBtL_T.txt".format(suffix))
    print('BtL model built {:.3f} sec...'.format(time.clock()-istart))

    print('Building scaled SVM models...'.format(suffix))
    temp = ModelBuilder([base+"trainfeaturesBtL_T.csv".format(suffix)],1)
    if downSample:
        temp.downSample()
    temp.buildScaler(base+"trainfeaturesBtLScaler_T.txt")
    temp.scaleData()
    temp.buildModelSVM(base+"modelSVMsBtL_T.txt")

    #Down-sample, scale data, apply PCA, and use SVM
    print('Building scaled PCA SVM models...')
    temp = ModelBuilder([base+"trainfeaturesBtL_T.csv"],1)
    if downSample:
        temp.downSample()
    temp.buildScaler(base+"trainfeaturesBtLScaler_T.txt")
    temp.scaleData()
    temp.buildDimensionReducer(base+"train/BtLReduce_T.txt",False)
    temp.reduceDimensions()
    temp.buildModelSVM(base+"modelSVMsrBtL_T.txt")

    #Down-sample, apply PCA with whitening, and use SVM
    print('Building PCA with whitening SVM models...')
    temp = ModelBuilder([base+"trainfeaturesBtL_T.csv"],1)
    if downSample:
        temp.downSample()
    temp.buildDimensionReducer(base+"train/BtLReduceW_T.txt",True)
    temp.reduceDimensions()
    temp.buildModelSVM(base+"modelSVMsrwBtL_T.txt")

    #Use other models
    print('Building other models...')
    temp = ModelBuilder([base+"trainfeaturesBtL_T.csv"],1)
    if downSample:
        temp.downSample()
    #Weighted SVM: Class 0 Weight: 1, Class 1 Weight: 2
    temp.buildModelSVM(base+"modelSVMcwBtL_T.txt",weights={0:2,1:3})

    temp = ModelBuilder([base+"trainfeaturesBtL_T.csv"],1)
    if downSample:
        temp.downSample()
    temp.buildScaler(base+"trainfeaturesBtLScaler_T.txt")
    temp.scaleData()
    temp.buildModelRF(base+"modelRF5BtL_T.txt",5)
    temp.buildModelRF(base+"modelRF10BtL_T.txt",10)
    temp.buildModelRF(base+"modelRF100BtL_T.txt",100)
    temp.buildModelRF(base+"modelRF200BtL_T.txt",200)
    temp.buildModelNB(base+"modelNBBtL_T.txt")

def buildTermModels(downSample=False):
    start = time.clock()
    istart = start
    #Down-sample and use SVM
    print('Building SVM models...')
    temp = ModelBuilder([base+"trainfeaturesBtL_T.csv"],1)
    print('Loaded model builder {:.3f} sec...'.format(time.clock()-start))
    if downSample:
        temp.downSample()
    temp.buildModelSVM(base+"modelSVMBtL_T.txt")
    print('BtL model built {:.3f} sec...'.format(time.clock()-istart))
    istart = time.clock()
    temp = ModelBuilder([base+"trainfeaturesWtK_T.csv"],1)
    if downSample:
        temp.downSample()
    temp.buildModelSVM(base+"modelSVMWtK_T.txt")
    print('WtKmodel built {:.3f} sec...'.format(time.clock()-istart))
    
    #Down-sample, scale data, and use SVM
    print('Building scaled SVM models...')
    temp = ModelBuilder([base+"trainfeaturesBtL_T.csv"],1)
    if downSample:
        temp.downSample()
    temp.buildScaler(base+"trainfeaturesBtLScaler_T.txt")
    temp.scaleData()
    temp.buildModelSVM(base+"modelSVMsBtL_T.txt")

    temp = ModelBuilder([base+"trainfeaturesWtK_T.csv"],1)
    temp.downSample()
    temp.buildScaler(base+"trainfeaturesWtKScaler_T.txt")
    temp.scaleData()
    temp.buildModelSVM(base+"modelSVMsWtK_T.txt")
    
    #Down-sample, scale data, apply PCA, and use SVM
    print('Building scaled PCA SVM models...')
    temp = ModelBuilder([base+"trainfeaturesBtL_T.csv"],1)
    if downSample:
        temp.downSample()
    temp.buildScaler(base+"trainfeaturesBtLScaler_T.txt")
    temp.scaleData()
    temp.buildDimensionReducer(base+"BtLReduce_T.txt",False)
    temp.reduceDimensions()
    temp.buildModelSVM(base+"modelSVMsrBtL_T.txt")

    temp = ModelBuilder([base+"trainfeaturesWtK_T.csv"],1)
    if downSample:
        temp.downSample()
    temp.buildScaler(base+"trainfeaturesWtKScaler_T.txt")
    temp.scaleData()
    temp.buildDimensionReducer(base+"WtKReduce_T.txt",False)
    temp.reduceDimensions()
    temp.buildModelSVM(base+"modelSVMsrWtK_T.txt")
    
    #Down-sample, apply PCA with whitening, and use SVM
    print('Building PCA with whitening SVM models...')
    temp = ModelBuilder([base+"trainfeaturesBtL_T.csv"],1)
    if downSample:
        temp.downSample()
    temp.buildDimensionReducer(base+"BtLReduceW_T.txt",True)
    temp.reduceDimensions()
    temp.buildModelSVM(base+"modelSVMsrwBtL_T.txt")

    temp = ModelBuilder([base+"trainfeaturesWtK_T.csv"],1)
    if downSample:
        temp.downSample()
    temp.buildDimensionReducer(base+"WtKReduceW_T.txt",True)
    temp.reduceDimensions()
    temp.buildModelSVM(base+"modelSVMsrwWtK_T.txt")
    
    #Use other models
    print('Building other models...')
    temp = ModelBuilder([base+"trainfeaturesBtL_T.csv"],1)
    if downSample:
        temp.downSample()
    #Weighted SVM: Class 0 Weight: 1, Class 1 Weight: 2
    temp.buildModelSVM(base+"modelSVMcwBtL_T.txt",weights={0:2,1:3})

    temp = ModelBuilder([base+"trainfeaturesWtK_T.csv"],1)
    if downSample:
        temp.downSample()
    #Weighted SVM: Class 0 Weight: 1, Class 1 Weight: 2
    temp.buildModelSVM(base+"modelSVMcwWtK_T.txt",weights={0:2,1:3})

    #5-Nearest Neighbors
    #temp = ModelBuilder([base+"trainfeaturesBtL_T.csv"],1)
    #temp.downSample()
    #temp.buildModelNeighbors(base+"modelNeighborsBtL_T.txt",5)
    #temp = ModelBuilder([base+"trainfeaturesWtK_T.csv"],1)
    #temp.downSample()
    #temp.buildModelNeighbors(base+"modelNeighborsWtK_T.txt",5)
    #Random forest of 10 trees
    temp = ModelBuilder([base+"trainfeaturesBtL_T.csv"],1)
    if downSample:
        temp.downSample()
    temp.buildScaler(base+"trainfeaturesBtLScaler_T.txt")
    temp.scaleData()
    #temp.buildModelRF(base+"modelRF10BtL_T.txt",10)
    temp.buildModelRF(base+"modelRF10BtL_T.txt",10)
    temp.buildModelRF(base+"modelRF5BtL_T.txt",5)
    temp.buildModelRF(base+"modelRF100BtL_T.txt",100)
    temp.buildModelRF(base+"modelRF200BtL_T.txt",200)
    temp.buildModelNB(base+"modelNBBtL_T.txt")
    
    temp = ModelBuilder([base+"trainfeaturesWtK_T.csv"],1)
    if downSample:
        temp.downSample()
    temp.buildScaler(base+"trainfeaturesWtKScaler_T.txt")
    temp.scaleData()
    #temp.buildModelRF(base+"modelRF10WtK_T.txt",10)
    temp.buildModelRF(base+"modelRF10WtK_T.txt",10)
    temp.buildModelRF(base+"modelRF5WtK_T.txt",5)
    temp.buildModelRF(base+"modelRF100WtK_T.txt",100)
    temp.buildModelRF(base+"modelRF200WtK_T.txt",200)
    temp.buildModelNB(base+"modelNBWtK_T.txt")
    print('Done! ')

def rebuildTermModels(downSample=False):
    temp = ModelBuilder([base+"trainfeaturesBtL_T.csv"],1)
    if downSample:
        temp.downSample()
    temp.buildScaler(base+"trainfeaturesBtLScaler_T.txt")
    temp.scaleData()
    #temp.buildModelRF(base+"modelRF10BtL_T.txt",10)
    temp.buildModelRF(base+"modelRF10BtL_T.txt",10)
    temp.buildModelRF(base+"modelRF5BtL_T.txt",5)

    temp = ModelBuilder([base+"trainfeaturesWtK_T.csv"],1)
    if downSample:
        temp.downSample()
    temp.buildScaler(base+"trainfeaturesWtKScaler_T.txt")
    temp.scaleData()
    #temp.buildModelRF(base+"modelRF10WtK_T.txt",10)
    temp.buildModelRF(base+"modelRF10WtK_T.txt",10)
    temp.buildModelRF(base+"modelRF5WtK_T.txt",5)
    
    #------------------------------
def evaluateTermModels():
    maxB = 0.0
    maxW = 0.0
    temp = ModelBuilder([base+"devfeaturesBtL_T.csv"],1)
    stats = temp.evaluateModel(base+"modelSVMBtL_T.txt")
    maxB = max(maxB, stats[0])
    printStats(stats, 'Unscaled SVM BtL')
    temp.setScaler(base+"trainfeaturesBtLScaler_T.txt")
    temp.scaleData()
    stats = temp.evaluateModel(base+"modelSVMsBtL_T.txt")
    maxB = max(maxB, stats[0])
    printStats(stats, 'Scaled SVM BtL')

    #stats = temp.evaluateModel(base+"modelNeighborsBtL_T.txt")
    #printStats(stats, 'Scaled NN BtL')
    stats = temp.evaluateModel(base+"modelRF5BtL_T.txt")
    maxB = max(maxB, stats[0])
    printStats(stats, 'Scaled RF5 BtL')
    stats = temp.evaluateModel(base+"modelRF10BtL_T.txt")
    maxB = max(maxB, stats[0])
    printStats(stats, 'Scaled RF10 BtL')
    stats = temp.evaluateModel(base+"modelRF100BtL_T.txt")
    maxB = max(maxB, stats[0])
    printStats(stats, 'Scaled RF100 BtL')
    stats = temp.evaluateModel(base+"modelRF200BtL_T.txt")
    maxB = max(maxB, stats[0])
    printStats(stats, 'Scaled RF200 BtL')
    stats = temp.evaluateModel(base+"modelNBBtL_T.txt")
    maxB = max(maxB, stats[0])
    printStats(stats, 'Scaled NB BtL')

    temp.setDimensionReducer(base+"BtLReduce_T.txt")
    temp.reduceDimensions()
    stats = temp.evaluateModel(base+"modelSVMsrBtL_T.txt")
    maxB = max(maxB, stats[0])
    printStats(stats, 'Scaled reduced SVM BtL')

    #temp.setData([base+"devfeaturesBtL.csv"])
    temp = ModelBuilder([base+"devfeaturesBtL_T.csv"],1)
    temp.setScaler(base+"trainfeaturesBtLScaler_T.txt")
    temp.scaleData()
    temp.setDimensionReducer(base+"BtLReduceW_T.txt")
    temp.reduceDimensions()
    stats = temp.evaluateModel(base+"modelSVMsrwBtL_T.txt")
    maxB = max(maxB, stats[0])
    printStats(stats, 'Scaled reduced PCA whitened SVM BtL')
    # --------------------------
    temp = ModelBuilder([base+"trainfeaturesWtK_T.csv"],1)
    temp.buildModelNeighbors(base+"modelNeighborsWtK_T.txt",5)
    temp = ModelBuilder([base+"devfeaturesWtK_T.csv"],1)
    stats = temp.evaluateModel(base+"modelSVMWtK_T.txt")
    maxW = max(maxW, stats[0])
    printStats(stats, 'Unscaled SVM WtK')
    
    temp.setScaler(base+"trainfeaturesWtKScaler_T.txt")
    temp.scaleData()
    stats = temp.evaluateModel(base+"modelSVMsWtK_T.txt")
    maxW = max(maxW, stats[0])
    printStats(stats, 'Scaled SVM WtK')

    #stats = temp.evaluateModel(base+"modelNeighborsWtK.txt")
    #printStats(stats, 'Scaled NN WtK')
    stats = temp.evaluateModel(base+"modelRF5WtK_T.txt")
    maxW = max(maxW, stats[0])
    printStats(stats, 'Scaled RF5 WtK')
    stats = temp.evaluateModel(base+"modelRF10WtK_T.txt")
    maxW = max(maxW, stats[0])
    printStats(stats, 'Scaled RF10 WtK')
    stats = temp.evaluateModel(base+"modelRF100WtK_T.txt")
    maxW = max(maxW, stats[0])
    printStats(stats, 'Scaled RF100 WtK')
    stats = temp.evaluateModel(base+"modelRF200WtK_T.txt")
    maxW = max(maxW, stats[0])
    printStats(stats, 'Scaled RF200 WtK')
    stats = temp.evaluateModel(base+"modelNBWtK_T.txt")
    maxW = max(maxW, stats[0])
    printStats(stats, 'Scaled NB WtK')

    temp.setDimensionReducer(base+"WtKReduce_T.txt")
    temp.reduceDimensions()
    stats = temp.evaluateModel(base+"modelSVMsrWtK_T.txt")
    maxW = max(maxW, stats[0])
    printStats(stats, 'Scaled reduced SVM WtK')

    temp = ModelBuilder([base+"devfeaturesWtK_T.csv"],1)
    temp.setScaler(base+"trainfeaturesWtKScaler_T.txt")
    temp.scaleData()
    temp.setDimensionReducer(base+"WtKReduceW_T.txt")
    temp.reduceDimensions()
    stats = temp.evaluateModel(base+"modelSVMsrwWtK_T.txt")
    maxW = max(maxW, stats[0])
    printStats(stats, 'Scaled reduced whitened SVM WtK')
    return [maxB, maxW]

def redoMF():
    start = time.clock()
    istart = start

    temp = ModelBuilder([base+"trainfeaturesBtL.csv"],1)
    temp.downSample()
    temp.buildScaler(base+"trainfeaturesBtLScaler.txt")
    temp.scaleData()
    dev = ModelBuilder([base+'devfeaturesBtL.csv'],1)
    dev.setScaler(base+"trainfeaturesBtLScaler.txt")
    dev.scaleData()
    r = 0.5
    while( r<0.92 ):
        temp.buildModelRF(base+"modelRF100BtL.txt",100)
        stats = dev.evaluateModel(base+"modelRF100BtL.txt")
        r = stats[1]
        printStats(stats, 'Scaled RF100 BtL')

    
#redoMF()
buildModels()
evaluateBtL()
evaluateWtK()
#buildTermModels()
#evaluateTermModels()
#[maxBtL, maxWtK] = evaluateTermModels()

#while( maxBtL<0.8 ):
#    buildTermModelsN(1)
#    [maxBtL, maxWtK] = evaluateTermModels()

#evaluateBtL()
#evaluateWtK()