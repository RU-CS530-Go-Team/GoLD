'''
Created on Nov 22, 2014

@author: ZDaniels
'''
from Feature import Feature
from gold.models.board import Board
import numpy as np
from scipy import signal

class LocalShapesFeature(Feature):

  def calculate_feature(self):
    '''startBoard = self.convert_board(self.start,0)'''
    startBoard1 = self.convert_board(self.start,1)
    startBoard2 = self.convert_board(self.start,-1)

    '''startBoard = self.convert_board(self.start,0)'''
    moveBoard1 = self.convert_board(self.move,1)
    moveBoard2 = self.convert_board(self.move,-1)


    '''print startBoard'''

    '''shape1 = np.array([[1,-1],[-1,1],[1,-1]])
    shape2 = np.array([[1,-1],[-1,-1],[-1,-1]])'''

    '''print (shape1 + shape2) / 2'''

    '''print self.is_shape_present(startBoard1,startBoard2,shape1,shape2)'''

    features1 = np.asarray(self.extract_template_information(startBoard1,startBoard2))
    features2 = np.asarray(self.extract_template_information(moveBoard1,moveBoard2))
    featuresDiff = features2 - features1

    features = list(features2)+list(featuresDiff)

    print len(features)

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
    convolvedBoard1 = signal.convolve2d(shapeV1,boardV1)
    convolvedBoard2 = signal.convolve2d(shapeV2,boardV2)
    convolvedBoardSum = convolvedBoard1 + convolvedBoard2
    targetNum = shapeV1.size * 2
    i,j = np.unravel_index(convolvedBoardSum.argmax(), convolvedBoardSum.shape)
    maxNum = convolvedBoardSum[i,j]
    return int(targetNum == maxNum)
