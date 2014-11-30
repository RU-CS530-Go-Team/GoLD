from sklearn import decomposition
import numpy as np
import pickle

class DictionaryBuilder():

  def __init__(self,dataFile,outputFile):
    data = np.loadtxt(open(dataFile,"rb"),delimiter=",",skiprows=0)
    dictionary = decomposition.MiniBatchDictionaryLearning(n_components=32, alpha=1, n_iter=500).fit(data)
    dictionaryData = pickle.dumps(dictionary)
    f = open(outputFile,"w")
    f.write(dictionaryData)
    f.close()