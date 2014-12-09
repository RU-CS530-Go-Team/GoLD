from gold.features.Feature import Feature
import numpy as np

class HuMomentsFeature(Feature):

  def calculate_feature(self):

    boardInput = self.convert_board(self.start,0,1,0)
    if self.rawMoment(boardInput,0,0) == 0:
      x_bar = 0
      y_bar = 0
      mu = 0
      n20 = 0
      n02 = 0
      n11 = 0
      n30 = 0
      n12 = 0
      n03 = 0
      n21 = 0
    else:
      x_bar = self.rawMoment(boardInput,1,0) / self.rawMoment(boardInput,0,0)
      y_bar = self.rawMoment(boardInput,0,1) / self.rawMoment(boardInput,0,0)
      mu = self.centralMoment(boardInput,0,0,x_bar,y_bar)
      n20 = self.siMoment(boardInput,2,0,x_bar,y_bar,mu)
      n02 = self.siMoment(boardInput,0,2,x_bar,y_bar,mu)
      n11 = self.siMoment(boardInput,1,1,x_bar,y_bar,mu)
      n30 = self.siMoment(boardInput,3,0,x_bar,y_bar,mu)
      n12 = self.siMoment(boardInput,1,2,x_bar,y_bar,mu)
      n03 = self.siMoment(boardInput,0,3,x_bar,y_bar,mu)
      n21 = self.siMoment(boardInput,2,1,x_bar,y_bar,mu)
    blackStart1 = n20 + n02
    blackStart2 = (n20 - n02)**2 + 4*n11**2
    blackStart3 = (n30 - 3*n12)**2 + (3*n21 - n03)**2
    blackStart4 = (n30 + n12)**2 + (n21 + n03)**2
    blackStart5 = (n30 - 3*n12)*(n30 + n12)*((n30 + n12)**2 - 3*(n21 + n03)**2) + (3*n21 - n03)*(n21 + n03)*(3*(n30 + n12)**2 - (n21 + n03)**2)
    blackStart6 = (n20 - n02)*((n30 + n12)**2 - (n21 + n03)**2) + 4*n11*(n30 + n12)*(n21 + n03)
    blackStart7 = (3*n21 - n03)*(n30 + n12)*((n30 + n12)**2 - 3*(n21 + n03)**2) - (n30 - 3*n12)*(n21 + n03)*(3*(n30 + n12)**2 - (n21 + n03)**2)
    blackStart8 = n11*((n30 + n12)**2 - (n03 + n21)**2) - (n20 - n02)*(n30 + n12)*(n03 + n21)

    boardInput = self.convert_board(self.start,0,0,1)
    if self.rawMoment(boardInput,0,0) == 0:
      x_bar = 0
      y_bar = 0
      mu = 0
      n20 = 0
      n02 = 0
      n11 = 0
      n30 = 0
      n12 = 0
      n03 = 0
      n21 = 0
    else:
      x_bar = self.rawMoment(boardInput,1,0) / self.rawMoment(boardInput,0,0)
      y_bar = self.rawMoment(boardInput,0,1) / self.rawMoment(boardInput,0,0)
      mu = self.centralMoment(boardInput,0,0,x_bar,y_bar)
      n20 = self.siMoment(boardInput,2,0,x_bar,y_bar,mu)
      n02 = self.siMoment(boardInput,0,2,x_bar,y_bar,mu)
      n11 = self.siMoment(boardInput,1,1,x_bar,y_bar,mu)
      n30 = self.siMoment(boardInput,3,0,x_bar,y_bar,mu)
      n12 = self.siMoment(boardInput,1,2,x_bar,y_bar,mu)
      n03 = self.siMoment(boardInput,0,3,x_bar,y_bar,mu)
      n21 = self.siMoment(boardInput,2,1,x_bar,y_bar,mu)
    whiteStart1 = n20 + n02
    whiteStart2 = (n20 - n02)**2 + 4*n11**2
    whiteStart3 = (n30 - 3*n12)**2 + (3*n21 - n03)**2
    whiteStart4 = (n30 + n12)**2 + (n21 + n03)**2
    whiteStart5 = (n30 - 3*n12)*(n30 + n12)*((n30 + n12)**2 - 3*(n21 + n03)**2) + (3*n21 - n03)*(n21 + n03)*(3*(n30 + n12)**2 - (n21 + n03)**2)
    whiteStart6 = (n20 - n02)*((n30 + n12)**2 - (n21 + n03)**2) + 4*n11*(n30 + n12)*(n21 + n03)
    whiteStart7 = (3*n21 - n03)*(n30 + n12)*((n30 + n12)**2 - 3*(n21 + n03)**2) - (n30 - 3*n12)*(n21 + n03)*(3*(n30 + n12)**2 - (n21 + n03)**2)
    whiteStart8 = n11*((n30 + n12)**2 - (n03 + n21)**2) - (n20 - n02)*(n30 + n12)*(n03 + n21)

    boardInput = self.convert_board(self.move,0,1,0)
    if self.rawMoment(boardInput,0,0) == 0:
      x_bar = 0
      y_bar = 0
      mu = 0
      n20 = 0
      n02 = 0
      n11 = 0
      n30 = 0
      n12 = 0
      n03 = 0
      n21 = 0
    else:
      x_bar = self.rawMoment(boardInput,1,0) / self.rawMoment(boardInput,0,0)
      y_bar = self.rawMoment(boardInput,0,1) / self.rawMoment(boardInput,0,0)
      mu = self.centralMoment(boardInput,0,0,x_bar,y_bar)
      n20 = self.siMoment(boardInput,2,0,x_bar,y_bar,mu)
      n02 = self.siMoment(boardInput,0,2,x_bar,y_bar,mu)
      n11 = self.siMoment(boardInput,1,1,x_bar,y_bar,mu)
      n30 = self.siMoment(boardInput,3,0,x_bar,y_bar,mu)
      n12 = self.siMoment(boardInput,1,2,x_bar,y_bar,mu)
      n03 = self.siMoment(boardInput,0,3,x_bar,y_bar,mu)
      n21 = self.siMoment(boardInput,2,1,x_bar,y_bar,mu)
    blackMove1 = n20 + n02
    blackMove2 = (n20 - n02)**2 + 4*n11**2
    blackMove3 = (n30 - 3*n12)**2 + (3*n21 - n03)**2
    blackMove4 = (n30 + n12)**2 + (n21 + n03)**2
    blackMove5 = (n30 - 3*n12)*(n30 + n12)*((n30 + n12)**2 - 3*(n21 + n03)**2) + (3*n21 - n03)*(n21 + n03)*(3*(n30 + n12)**2 - (n21 + n03)**2)
    blackMove6 = (n20 - n02)*((n30 + n12)**2 - (n21 + n03)**2) + 4*n11*(n30 + n12)*(n21 + n03)
    blackMove7 = (3*n21 - n03)*(n30 + n12)*((n30 + n12)**2 - 3*(n21 + n03)**2) - (n30 - 3*n12)*(n21 + n03)*(3*(n30 + n12)**2 - (n21 + n03)**2)
    blackMove8 = n11*((n30 + n12)**2 - (n03 + n21)**2) - (n20 - n02)*(n30 + n12)*(n03 + n21)

    boardInput = self.convert_board(self.move,0,0,1)
    if self.rawMoment(boardInput,0,0) == 0:
      x_bar = 0
      y_bar = 0
      mu = 0
      n20 = 0
      n02 = 0
      n11 = 0
      n30 = 0
      n12 = 0
      n03 = 0
      n21 = 0
    else:
      x_bar = self.rawMoment(boardInput,1,0) / self.rawMoment(boardInput,0,0)
      y_bar = self.rawMoment(boardInput,0,1) / self.rawMoment(boardInput,0,0)
      mu = self.centralMoment(boardInput,0,0,x_bar,y_bar)
      n20 = self.siMoment(boardInput,2,0,x_bar,y_bar,mu)
      n02 = self.siMoment(boardInput,0,2,x_bar,y_bar,mu)
      n11 = self.siMoment(boardInput,1,1,x_bar,y_bar,mu)
      n30 = self.siMoment(boardInput,3,0,x_bar,y_bar,mu)
      n12 = self.siMoment(boardInput,1,2,x_bar,y_bar,mu)
      n03 = self.siMoment(boardInput,0,3,x_bar,y_bar,mu)
      n21 = self.siMoment(boardInput,2,1,x_bar,y_bar,mu)
    whiteMove1 = n20 + n02
    whiteMove2 = (n20 - n02)**2 + 4*n11**2
    whiteMove3 = (n30 - 3*n12)**2 + (3*n21 - n03)**2
    whiteMove4 = (n30 + n12)**2 + (n21 + n03)**2
    whiteMove5 = (n30 - 3*n12)*(n30 + n12)*((n30 + n12)**2 - 3*(n21 + n03)**2) + (3*n21 - n03)*(n21 + n03)*(3*(n30 + n12)**2 - (n21 + n03)**2)
    whiteMove6 = (n20 - n02)*((n30 + n12)**2 - (n21 + n03)**2) + 4*n11*(n30 + n12)*(n21 + n03)
    whiteMove7 = (3*n21 - n03)*(n30 + n12)*((n30 + n12)**2 - 3*(n21 + n03)**2) - (n30 - 3*n12)*(n21 + n03)*(3*(n30 + n12)**2 - (n21 + n03)**2)
    whiteMove8 = n11*((n30 + n12)**2 - (n03 + n21)**2) - (n20 - n02)*(n30 + n12)*(n03 + n21)

    return [blackMove1, blackMove2, blackMove3, blackMove4, blackMove5, blackMove6, blackMove7, blackMove8, whiteMove1, whiteMove2, whiteMove3, whiteMove4, whiteMove5, whiteMove6, whiteMove7, whiteMove8, blackMove1 - blackStart1, blackMove2 - blackStart2, blackMove3 - blackStart3, blackMove4 - blackStart4, blackMove5 - blackStart5, blackMove6 - blackStart6, blackMove7 - blackStart7, blackMove8 - blackStart8, whiteMove1 - whiteStart1, whiteMove2 - whiteStart2, whiteMove3 - whiteStart3, whiteMove4 - whiteStart4, whiteMove5 - whiteStart5, whiteMove6 - whiteStart6, whiteMove7 - whiteStart7, whiteMove8 - whiteStart8]

  def convert_board(self,boardInput,blankVal,blackVal,whiteVal):
    boardOutput = np.zeros((boardInput.x,boardInput.y))
    for i in range(boardInput.x):
      for q in range(boardInput.y):
        if (i, q) in boardInput.white_stones:
          boardOutput[i][q] = whiteVal
        elif (i, q) in boardInput.black_stones:
          boardOutput[i][q] = blackVal
        else:
          boardOutput[i][q] = blankVal
    return boardOutput

  def rawMoment(self,boardInput,p,q):
    M = 0
    for i in range(boardInput.shape[1]):
      for j in range(boardInput.shape[0]):
        M = M + (i**p)*(j**q)*boardInput[j][i]
    return float(M)

  def centralMoment(self,boardInput,p,q,x_bar,y_bar):
    M = 0
    for i in range(boardInput.shape[1]):
      for j in range(boardInput.shape[0]):
        M = M + ((i-x_bar)**p)*((j-y_bar)**q)*boardInput[j][i]
    return float(M)

  def siMoment(self,boardInput,p,q,x_bar,y_bar,mu):
    return float((self.centralMoment(boardInput,p,q,x_bar,y_bar))/(mu**(1 +((p+q)/2))))
