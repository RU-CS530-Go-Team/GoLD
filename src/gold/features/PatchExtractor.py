'''
Created on Nov 29, 2014

@author: ZDaniels
'''
from Feature import Feature
from sklearn import decomposition
from sklearn.feature_extraction import image
import numpy as np

class PatchExtractor(Feature):

  def calculate_feature(self):
    moveConverted = self.convert_board(self.move,0)
    patch_size = (4, 4)
    data = image.extract_patches_2d(moveConverted,patch_size)
    data = data.reshape(data.shape[0], -1)
    moveConverted = np.rot90(moveConverted)
    data2 = image.extract_patches_2d(moveConverted,patch_size)
    data2 = data2.reshape(data2.shape[0], -1)
    data = np.concatenate((data, data2), axis=0)
    moveConverted = np.rot90(moveConverted)
    data2 = image.extract_patches_2d(moveConverted,patch_size)
    data2 = data2.reshape(data2.shape[0], -1)
    data = np.concatenate((data, data2), axis=0)
    moveConverted = np.rot90(moveConverted)
    data2 = image.extract_patches_2d(moveConverted,patch_size)
    data2 = data2.reshape(data2.shape[0], -1)
    data = np.concatenate((data, data2), axis=0)
    moveConverted = np.rot90(moveConverted)
    moveConverted = np.fliplr(moveConverted)
    data2 = image.extract_patches_2d(moveConverted,patch_size)
    data2 = data2.reshape(data2.shape[0], -1)
    data = np.concatenate((data, data2), axis=0)
    moveConverted = np.rot90(moveConverted)
    data2 = image.extract_patches_2d(moveConverted,patch_size)
    data2 = data2.reshape(data2.shape[0], -1)
    data = np.concatenate((data, data2), axis=0)
    moveConverted = np.rot90(moveConverted)
    data2 = image.extract_patches_2d(moveConverted,patch_size)
    data2 = data2.reshape(data2.shape[0], -1)
    data = np.concatenate((data, data2), axis=0)
    moveConverted = np.rot90(moveConverted)
    data2 = image.extract_patches_2d(moveConverted,patch_size)
    data2 = data2.reshape(data2.shape[0], -1)
    data = np.concatenate((data, data2), axis=0)
    return data

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