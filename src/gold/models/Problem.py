'''
Created on Nov 1, 2014

@author: Zac1164
@author: JBlackmore
'''
import re

from gold.models.board import Board


class Problem:
    '''
    classdocs
    '''
    start=None

    def __init__(self, sgffile):
        '''
        Constructor
        '''
        self.loadSGF(sgffile)
    
    def loadSGF(self, sgffile):

        size = 19
        
        currentGame = open(sgffile)
        
        gameData = currentGame.read()
        
        boardSizeLocation = gameData.find("SZ")
        sizeString = ''
        counter = 0
        currentChar = gameData[boardSizeLocation + counter + 3]
        while(currentChar != ']'):
            sizeString += currentChar
            counter += 1
            currentChar = gameData[boardSizeLocation + counter + 3]
        
        if(sizeString.isdigit()):
            size = int(sizeString)
        
        currentBoard = Board(size,size)
        
        whitePositionLocations = [m.start() for m in re.finditer('AW', gameData)]
        blackPositionLocations = [m.start() for m in re.finditer('AB', gameData)]
        
        stonePositions = whitePositionLocations + blackPositionLocations
        stonePositions.sort()
        
        for i in stonePositions:
            isBlack = False
            if i in blackPositionLocations:
                isBlack = True
            counter = 0
            while(True):
                currentChar = gameData[i + counter + 2]
                if (currentChar != '['):
                    break
                currentChar = gameData[i + counter + 3]
                y = ord(currentChar) - ord('a')
                currentChar = gameData[i + counter + 4]
                x = ord(currentChar) - ord('a')
                currentBoard.place_stone(x,y,isBlack)
                counter += 4
        
        print currentBoard
        self.start = currentBoard
        currentGame.close()


