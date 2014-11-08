'''
Created on Nov 6, 2014

@author: Zac1164
'''

from array import array

import re

class MoveTreeParser:

  blackFirst = True
  moveID = None
  parent = None
  solutionStates = None
  terminalStates = None


  def __init__(self, gameFile):
    self.moveID = {}
    self.parent = {}
    self.solutionStates = []
    self.terminalStates = []

    currentGame = open(gameFile)

    gameData = currentGame.read()
    gameData = gameData.replace("\n", "")
    gameData = gameData.replace("\r", "")
    gameData = gameData.replace(" ", "")

    firstBlackMove = gameData.find(';B')
    firstWhiteMove = gameData.find(';W')

    if (firstBlackMove > firstWhiteMove):
      self.blackFirst = False

    position = 0

    if self.blackFirst:
      position = gameData.find('(;B')
      if position != firstBlackMove - 1:
        gameData = gameData[:firstBlackMove]+"("+gameData[firstBlackMove:]
        position = firstBlackMove
    else:
      position = gameData.find('(;W')
      if position != firstWhiteMove - 1:
        gameData = gameData[:firstWhiteMove]+"("+gameData[firstWhiteMove:]
        position = firstWhiteMove

    currentMoveSet = ""
    currentParent = 0
    maxMoveID = 0

    branchNodes = []
    branchNodes.append(-1)
    '''Match Opening Parenthesis'''

    while (position < len(gameData)):
      currentChar = gameData[position]
      position += 1
      if currentChar == "(":
        if currentMoveSet != "":
          currentMoveSet = currentMoveSet[0:5]
          maxMoveID += 1
          self.moveID[maxMoveID] = currentMoveSet
          self.parent[maxMoveID] = currentParent
          currentParent = maxMoveID
          currentMoveSet = ""
        branchNodes.append(currentParent)
      elif currentChar == ";":
        if currentMoveSet != "":
          currentMoveSet = currentMoveSet[0:5]
          maxMoveID += 1
          self.moveID[maxMoveID] = currentMoveSet
          self.parent[maxMoveID] = currentParent
          currentParent = maxMoveID
          currentMoveSet = ""
      elif currentChar == ")":
        if currentMoveSet != "":
          currentMoveSet = currentMoveSet[0:5]
          maxMoveID += 1
          self.moveID[maxMoveID] = currentMoveSet
          self.parent[maxMoveID] = currentParent
          currentMoveSet = ""
          self.terminalStates.append(maxMoveID)
        currentParent = branchNodes.pop()
      elif currentChar == "\r" or currentChar == "\n" or currentChar == " ":
        continue
      elif currentChar == "C":
        finalSquareBracketPosition = gameData.find(']',position-1)
        if gameData.find('RIGHT',position-1,finalSquareBracketPosition) != -1:
          currentMoveSet = currentMoveSet[0:5]
          maxMoveID += 1
          self.moveID[maxMoveID] = currentMoveSet
          self.parent[maxMoveID] = currentParent
          currentParent = maxMoveID
          currentMoveSet = ""
          self.solutionStates.append(maxMoveID)
          self.terminalStates.append(maxMoveID)
        position = finalSquareBracketPosition + 1
      else:
        currentMoveSet += currentChar
    currentGame.close()

  def getTerminalStates(self):
    return self.terminalStates

  def getSolutionStates(self):
    return self.solutionStates

  def getTerminalIncorrectStates(self):
    terminalStatesSet = set(self.terminalStates)
    solutionStatesSet = set(self.solutionStates)
    return terminalStatesSet.difference(solutionStatesSet)

  def getSolutionNodes(self):
    solutionNodes = []
    for node in self.solutionStates:
      parentNode = self.parent[node]
      solutionNodes.append(node)
      while parentNode != 0:
        solutionNodes.append(parentNode)
        parentNode = self.parent[parentNode]
    return set(solutionNodes)

  def getIncorrectNodes(self):
    solutionNodes = self.getSolutionNodes()
    allNodes = set(self.moveID.keys())
    return allNodes.difference(solutionNodes)

  def getMove(self,ID):
    return self.moveID[ID]

  def formatMove(self,moveString):
    move = {'isBlack':False,'x':0,'y':0}
    if moveString[0] == 'B':
      move['isBlack'] = True
    move['x'] = ord(moveString[3]) - ord('a')
    move['y'] = ord(moveString[2]) - ord('a')
    return move

  def getParent(self,ID):
    return self.parent[ID]

  def getAllPaths(self):
    paths = []
    for node in self.terminalStates:
      currentPath = []
      parentNode = self.parent[node]
      currentPath.append(node)
      while parentNode != 0:
        currentPath.append(parentNode)
        parentNode = self.parent[parentNode]
      currentPath.reverse()
      paths.append(currentPath)
    return paths

  def printAllPaths(self):
    paths = self.getAllPaths()
    for path in paths:
      for node in path:
        print self.getMove(node)
      print "\n"
