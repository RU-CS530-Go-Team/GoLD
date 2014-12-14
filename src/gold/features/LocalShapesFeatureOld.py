'''
Created on Nov 22, 2014

@author: ZDaniels
'''
from Feature import Feature
from gold.models.board import Board
import numpy as np
from scipy import signal
from gold.learn.FeatureSelector import FeatureSelector
from gold.learn.Model import ModelBuilder
from gold.learn.Model import Model
import pickle

class LocalShapeModelGenerator():

  def __init__(self,dataFileList,outputFile):
    temp = ModelBuilder(dataFileList)
    temp.downSample()
    temp.buildModelSVM(outputFile)

class LocalShapesSelector():

  def __init__(self,dataFileListBtL,dataFileListWtK,numBaseFeatures,outputFile1,outputFile2):
    featureSel = FeatureSelector(dataFileListBtL,False)
    numDimensions = featureSel.instances.shape[1]
    numShapes = numDimensions/2
    featureSet1b = featureSel.selectFeaturesFromSubset(list(range(numShapes)),numBaseFeatures)
    featureSet2b = featureSel.selectFeaturesFromSubset(list(range(numShapes,numDimensions)),numBaseFeatures)
    featureSetb = list(set(list(featureSet1b) + list(featureSet2b)))
    featureSel = FeatureSelector(dataFileListWtK,False)
    featureSet1w = featureSel.selectFeaturesFromSubset(list(range(numShapes)),numBaseFeatures)
    featureSet2w = featureSel.selectFeaturesFromSubset(list(range(numShapes,numDimensions)),numBaseFeatures)
    featureSetw = list(set(list(featureSet1w) + list(featureSet2w)))
    featureSet = list(set(list(featureSetb) + list(featureSetw)))
    self.generate_templates(featureSet,outputFile1,outputFile2)

  def generate_templates(self,featureSet,outputFile1,outputFile2):
    shapeIndex = 0
    shapeSet1 = []
    shapeSet2 = []
    '''2x2'''
    shape1 = np.zeros((2,2))
    shape2 = np.zeros((2,2))
    for i in range(-1,2):
      if i == 0:
        shape1[0,0] = -1
        shape2[0,0] = 1
      else:
        shape1[0,0] = i
        shape2[0,0] = i
      for j in range(-1,2):
        if i == 0:
          shape1[0,1] = -1
          shape2[0,1] = 1
        else:
          shape1[0,1] = j
          shape2[0,1] = j
        for k in range(-1,2):
          if k == 0:
            shape1[1,0] = -1
            shape2[1,0] = 1
          else:
            shape1[1,0] = k
            shape2[1,0] = k
          for l in range(-1,2):
            if l == 0:
              shape1[1,1] = -1
              shape2[1,1] = 1
            else:
              shape1[1,1] = l
              shape2[1,1] = l
            if shapeIndex in featureSet:
              shapeSet1.append(np.copy(shape1))
              shapeSet2.append(np.copy(shape2))
            shapeIndex = shapeIndex + 1
    '''2x3'''
    shape1 = np.zeros((2,3))
    shape2 = np.zeros((2,3))
    for i in range(-1,2):
      if i == 0:
        shape1[0,0] = -1
        shape2[0,0] = 1
      else:
        shape1[0,0] = i
        shape2[0,0] = i
      for j in range(-1,2):
        if i == 0:
          shape1[0,1] = -1
          shape2[0,1] = 1
        else:
          shape1[0,1] = j
          shape2[0,1] = j
        for k in range(-1,2):
          if k == 0:
            shape1[1,0] = -1
            shape2[1,0] = 1
          else:
            shape1[1,0] = k
            shape2[1,0] = k
          for l in range(-1,2):
            if l == 0:
              shape1[1,1] = -1
              shape2[1,1] = 1
            else:
              shape1[1,1] = l
              shape2[1,1] = l
            for m in range(-1,2):
              if m == 0:
                shape1[0,2] = -1
                shape2[0,2] = 1
              else:
                shape1[0,2] = m
                shape2[0,2] = m
              for n in range(-1,2):
                if n == 0:
                  shape1[1,2] = -1
                  shape2[1,2] = 1
                else:
                  shape1[1,2] = n
                  shape2[1,2] = n
                if shapeIndex in featureSet:
                  shapeSet1.append(np.copy(shape1))
                  shapeSet2.append(np.copy(shape2))
                shapeIndex = shapeIndex + 1
    '''3x2'''
    shape1 = np.zeros((3,2))
    shape2 = np.zeros((3,2))
    for i in range(-1,2):
      if i == 0:
        shape1[0,0] = -1
        shape2[0,0] = 1
      else:
        shape1[0,0] = i
        shape2[0,0] = i
      for j in range(-1,2):
        if i == 0:
          shape1[0,1] = -1
          shape2[0,1] = 1
        else:
          shape1[0,1] = j
          shape2[0,1] = j
        for k in range(-1,2):
          if k == 0:
            shape1[1,0] = -1
            shape2[1,0] = 1
          else:
            shape1[1,0] = k
            shape2[1,0] = k
          for l in range(-1,2):
            if l == 0:
              shape1[1,1] = -1
              shape2[1,1] = 1
            else:
              shape1[1,1] = l
              shape2[1,1] = l
            for m in range(-1,2):
              if m == 0:
                shape1[2,0] = -1
                shape2[2,0] = 1
              else:
                shape1[2,0] = m
                shape2[2,0] = m
              for n in range(-1,2):
                if n == 0:
                  shape1[2,1] = -1
                  shape2[2,1] = 1
                else:
                  shape1[2,1] = n
                  shape2[2,1] = n
                if shapeIndex in featureSet:
                  shapeSet1.append(np.copy(shape1))
                  shapeSet2.append(np.copy(shape2))
                shapeIndex = shapeIndex + 1
    shapeData = pickle.dumps(shapeSet1)
    f = open(outputFile1,"w")
    f.write(shapeData)
    f.close()
    shapeData = pickle.dumps(shapeSet2)
    f = open(outputFile2,"w")
    f.write(shapeData)
    f.close()

class LocalShapesFeature(Feature):

  def calculate_feature(self, dataDir=None):
    '''startBoard = self.convert_board(self.start,0)'''
    startBoard1 = self.convert_board(self.start,1)
    startBoard2 = self.convert_board(self.start,-1)

    '''startBoard = self.convert_board(self.start,0)'''
    moveBoard1 = self.convert_board(self.move,1)
    moveBoard2 = self.convert_board(self.move,-1)

    if dataDir==None:
      dataDir = self.dataDir
    else:
      self.dataDir = dataDir

    '''print startBoard'''

    '''shape1 = np.array([[1,-1],[-1,1],[1,-1]])
    shape2 = np.array([[1,-1],[-1,-1],[-1,-1]])'''

    '''print (shape1 + shape2) / 2'''

    '''print self.is_shape_present(startBoard1,startBoard2,shape1,shape2)'''

    #features1 = np.asarray(self.extract_template_information(startBoard1,startBoard2))
    #features2 = np.asarray(self.extract_template_information(moveBoard1,moveBoard2))

    self.set_shape_templates(dataDir+"shapeSet1.txt",dataDir+"shapeSet2.txt")

    features1 = np.asarray(self.extract_features(startBoard1,startBoard2))
    features2 = np.asarray(self.extract_features(moveBoard1,moveBoard2))

    featuresDiff = features2 - features1

    features = list(features2)+list(featuresDiff)

    return features

    '''model = None

    if self.isblack:
      model = Model(dataDir+"localShapeModelBtL.txt",0)
    else:
      model = Model(dataDir+"localShapeModelWtK.txt",0)

    return model.getScoreCorrect(features)'''

  def set_shape_templates(self,shapeFile1,shapeFile2):
    f = open(shapeFile1)
    shapeSet1Data = f.read()
    f.close()
    self.shapeSet1 = pickle.loads(shapeSet1Data)
    f = open(shapeFile2)
    shapeSet2Data = f.read()
    f.close()
    self.shapeSet2 = pickle.loads(shapeSet2Data)

  def extract_features(self,boardV1,boardV2):
    features = []
    for shape in range(len(self.shapeSet1)):
      features.append(self.is_shape_present(boardV1,boardV2,self.shapeSet1[shape],self.shapeSet2[shape]))
    return features

  def convert_board(self,boardInput,blankVal):
    boardOutput = np.zeros((boardInput.x,boardInput.y))
    for i in range(boardInput.x):
      for q in range(boardInput.y):
        if (i, q) in boardInput.white_stones:
          boardOutput[i][q] = -1
        elif (i, q) in boardInput.black_stones:
          boardOutput[i][q] = 1
        else:
          boardOutput[i][q] = blankVal
    return boardOutput

  def extract_template_information(self,boardV1,boardV2):
    features = []
    '''2x2'''
    shape1 = np.zeros((2,2))
    shape2 = np.zeros((2,2))
    for i in range(-1,2):
      if i == 0:
        shape1[0,0] = -1
        shape2[0,0] = 1
      else:
        shape1[0,0] = i
        shape2[0,0] = i
      for j in range(-1,2):
        if i == 0:
          shape1[0,1] = -1
          shape2[0,1] = 1
        else:
          shape1[0,1] = j
          shape2[0,1] = j
        for k in range(-1,2):
          if k == 0:
            shape1[1,0] = -1
            shape2[1,0] = 1
          else:
            shape1[1,0] = k
            shape2[1,0] = k
          for l in range(-1,2):
            if l == 0:
              shape1[1,1] = -1
              shape2[1,1] = 1
            else:
              shape1[1,1] = l
              shape2[1,1] = l
            features.append(self.is_shape_present(boardV1,boardV2,shape1,shape2))
    '''2x3'''
    shape1 = np.zeros((2,3))
    shape2 = np.zeros((2,3))
    for i in range(-1,2):
      if i == 0:
        shape1[0,0] = -1
        shape2[0,0] = 1
      else:
        shape1[0,0] = i
        shape2[0,0] = i
      for j in range(-1,2):
        if i == 0:
          shape1[0,1] = -1
          shape2[0,1] = 1
        else:
          shape1[0,1] = j
          shape2[0,1] = j
        for k in range(-1,2):
          if k == 0:
            shape1[1,0] = -1
            shape2[1,0] = 1
          else:
            shape1[1,0] = k
            shape2[1,0] = k
          for l in range(-1,2):
            if l == 0:
              shape1[1,1] = -1
              shape2[1,1] = 1
            else:
              shape1[1,1] = l
              shape2[1,1] = l
            for m in range(-1,2):
              if m == 0:
                shape1[0,2] = -1
                shape2[0,2] = 1
              else:
                shape1[0,2] = m
                shape2[0,2] = m
              for n in range(-1,2):
                if n == 0:
                  shape1[1,2] = -1
                  shape2[1,2] = 1
                else:
                  shape1[1,2] = n
                  shape2[1,2] = n
                features.append(self.is_shape_present(boardV1,boardV2,shape1,shape2))
    '''3x2'''
    shape1 = np.zeros((3,2))
    shape2 = np.zeros((3,2))
    for i in range(-1,2):
      if i == 0:
        shape1[0,0] = -1
        shape2[0,0] = 1
      else:
        shape1[0,0] = i
        shape2[0,0] = i
      for j in range(-1,2):
        if i == 0:
          shape1[0,1] = -1
          shape2[0,1] = 1
        else:
          shape1[0,1] = j
          shape2[0,1] = j
        for k in range(-1,2):
          if k == 0:
            shape1[1,0] = -1
            shape2[1,0] = 1
          else:
            shape1[1,0] = k
            shape2[1,0] = k
          for l in range(-1,2):
            if l == 0:
              shape1[1,1] = -1
              shape2[1,1] = 1
            else:
              shape1[1,1] = l
              shape2[1,1] = l
            for m in range(-1,2):
              if m == 0:
                shape1[2,0] = -1
                shape2[2,0] = 1
              else:
                shape1[2,0] = m
                shape2[2,0] = m
              for n in range(-1,2):
                if n == 0:
                  shape1[2,1] = -1
                  shape2[2,1] = 1
                else:
                  shape1[2,1] = n
                  shape2[2,1] = n
                features.append(self.is_shape_present(boardV1,boardV2,shape1,shape2))
    '''3x3'''
    '''shape1 = np.zeros((3,3))
    shape2 = np.zeros((3,3))
    for i in range(-1,2):
      if i == 0:
        shape1[0,0] = -1
        shape2[0,0] = 1
      else:
        shape1[0,0] = i
        shape2[0,0] = i
      for j in range(-1,2):
        if i == 0:
          shape1[0,1] = -1
          shape2[0,1] = 1
        else:
          shape1[0,1] = j
          shape2[0,1] = j
        for k in range(-1,2):
          if k == 0:
            shape1[1,0] = -1
            shape2[1,0] = 1
          else:
            shape1[1,0] = k
            shape2[1,0] = k
          for l in range(-1,2):
            if l == 0:
              shape1[1,1] = -1
              shape2[1,1] = 1
            else:
              shape1[1,1] = l
              shape2[1,1] = l
            for m in range(-1,2):
              if m == 0:
                shape1[0,2] = -1
                shape2[0,2] = 1
              else:
                shape1[0,2] = m
                shape2[0,2] = m
              for n in range(-1,2):
                if n == 0:
                  shape1[1,2] = -1
                  shape2[1,2] = 1
                else:
                  shape1[1,2] = n
                  shape2[1,2] = n
                for o in range(-1,2):
                  if o == 0:
                    shape1[2,0] = -1
                    shape2[2,0] = 1
                  else:
                    shape1[2,0] = o
                    shape2[2,0] = o
                  for p in range(-1,2):
                    if p == 0:
                      shape1[2,1] = -1
                      shape2[2,1] = 1
                    else:
                      shape1[2,1] = p
                      shape2[2,1] = p
                    for q in range(-1,2):
                      if q == 0:
                        shape1[2,2] = -1
                        shape2[2,2] = 1
                      else:
                        shape1[2,2] = q
                        shape2[2,2] = q
                      features.append(self.is_shape_present(boardV1,boardV2,shape1,shape2))'''
    return features

  def is_shape_present(self,boardV1,boardV2,shapeV1,shapeV2):
    featureVal = self.is_shape_present_helper(boardV1,boardV2,shapeV1,shapeV2)
    if not (featureVal):
      shapeV1 = np.rot90(shapeV1)
      shapeV2 = np.rot90(shapeV2)
      featureVal = self.is_shape_present_helper(boardV1,boardV2,shapeV1,shapeV2)
    if not (featureVal):
      shapeV1 = np.rot90(shapeV1)
      shapeV2 = np.rot90(shapeV2)
      featureVal = self.is_shape_present_helper(boardV1,boardV2,shapeV1,shapeV2)
    if not (featureVal):
      shapeV1 = np.rot90(shapeV1)
      shapeV2 = np.rot90(shapeV2)
      featureVal = self.is_shape_present_helper(boardV1,boardV2,shapeV1,shapeV2)
    if not (featureVal):
      shapeV1 = np.rot90(shapeV1)
      shapeV1 = np.fliplr(shapeV1)
      shapeV2 = np.rot90(shapeV2)
      shapeV2 = np.fliplr(shapeV2)
      featureVal = self.is_shape_present_helper(boardV1,boardV2,shapeV1,shapeV2)
    if not (featureVal):
      shapeV1 = np.rot90(shapeV1)
      shapeV2 = np.rot90(shapeV2)
      featureVal = self.is_shape_present_helper(boardV1,boardV2,shapeV1,shapeV2)
    if not (featureVal):
      shapeV1 = np.rot90(shapeV1)
      shapeV2 = np.rot90(shapeV2)
      featureVal = self.is_shape_present_helper(boardV1,boardV2,shapeV1,shapeV2)
    if not (featureVal):
      shapeV1 = np.rot90(shapeV1)
      shapeV2 = np.rot90(shapeV2)
      featureVal = self.is_shape_present_helper(boardV1,boardV2,shapeV1,shapeV2)
    return int(featureVal)

  def is_shape_present_helper(self,boardV1,boardV2,shapeV1,shapeV2):
    convolvedBoard1 = signal.convolve2d(shapeV1,boardV1)
    convolvedBoard2 = signal.convolve2d(shapeV2,boardV2)
    convolvedBoardSum = convolvedBoard1 + convolvedBoard2
    targetNum = shapeV1.size * 2
    i,j = np.unravel_index(convolvedBoardSum.argmax(), convolvedBoardSum.shape)
    maxNum = convolvedBoardSum[i,j]
    return (targetNum == maxNum)
