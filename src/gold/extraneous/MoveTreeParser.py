'''
Created on Nov 6, 2014

@author: Zac1164
'''

from array import array
from gold.models.board import Board
import re

class UnspecifiedProblemType(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class MoveTreeParser():

  def __init__(self, gameFile):
    self.blackFirst = True
    self.problemType = 0
    self.flipColors = False
    self.boardDimensions = None
    self.moveID = {}
    self.parent = {}
    self.solutionStates = []
    self.terminalStates = []
    self.boardDimensions = {'xMin':0,'xMax':0,'yMin':0,'yMax':0}

    currentGame = open(gameFile)

    gameData = currentGame.read()
    gameData = gameData.replace("\n", "")
    gameData = gameData.replace("\r", "")
    gameData = gameData.replace(" ", "")

    firstBlackMove = gameData.find(';B')
    firstWhiteMove = gameData.find(';W')

    if (firstBlackMove > firstWhiteMove or firstBlackMove<0):
      self.blackFirst = False
    else:
      self.blackFirst = True
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


    self.computeProblemType(gameData,position)

    if self.problemType == 0:
      raise UnspecifiedProblemType("No Specified Problem Type")
      #if not self.blackFirst:
       # self.flipColors = True

    if self.problemType == 2 or self.problemType == 3:
      self.flipColors = True

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
          if len(currentMoveSet)<5:
            print('No move to comment on')
          else:
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

    self.computeBoardDimensions(gameData)
    self.start = self.parseStartState(gameData)
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
      while parentNode > 0:
        solutionNodes.append(parentNode)
        parentNode = self.parent[parentNode]
    return set(solutionNodes)

  def getIncorrectNodes(self):
    solutionNodes = self.getSolutionNodes()
    allNodes = set(self.moveID.keys())
    return allNodes.difference(solutionNodes)

  def getMove(self,ID):
    if self.moveID[ID] == None:
      raise Exception('There is no move for ID={}'.format(ID))
    return self.moveID[ID]

  def formatMove(self,moveString):
    move = {'isBlack':False,'x':0,'y':0}
    if moveString[0] == 'B' and not self.flipColors:
      move['isBlack'] = True
    if moveString[0] == 'W' and self.flipColors:
      move['isBlack'] = True
    move['x'] = ord(moveString[3]) - ord('a') - self.boardDimensions['xMin']
    move['y'] = ord(moveString[2]) - ord('a') - self.boardDimensions['yMin']
    return move

  def getParent(self,ID):
    return self.parent[ID]

  def getAllPaths(self):
    paths = []
    for node in self.terminalStates:
      currentPath = []
      parentNode = self.parent[node]
      currentPath.append(node)
      while parentNode > 0:
        currentPath.append(parentNode)
        parentNode = self.parent[parentNode]
      currentPath.reverse()
      paths.append(currentPath)
    return paths

  def getSolutionPaths(self):
    paths = []
    for node in self.solutionStates:
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
        print (self.getMove(node))
      print ("\n")

  def getProblemType(self):
    return self.problemType

  def isColorFlipped(self):
    return self.flipColors

  def getProblemTypeDesc(self):
    descArr = ['No Type', 'Black to Live', 'Black to Kill', 'White to Live', 'White to Kill']
    return descArr[self.problemType]

  def computeProblemType(self,gameData,firstMovePosition):
    minIndex = firstMovePosition

    gameData = gameData.lower()

    '''No Type: 0'''
    '''Black To Live: 1'''
    tempSet = set()
    tempSet.add(gameData.find('blacktolive',0,firstMovePosition))
    tempSet.add(gameData.find('blacklives',0,firstMovePosition))
    tempSet.add(gameData.find('blacktoplayandlive',0,firstMovePosition))
    tempSet.add(gameData.find('blackplaysandlives',0,firstMovePosition))
    tempSet.add(gameData.find('blacktotryandlive',0,firstMovePosition))
    tempSet.add(gameData.find('blacktodohisbesttolive',0,firstMovePosition))
    tempSet.add(gameData.find('blacktoscrapeoutameagerexistence',0,firstMovePosition))
    tempSet.add(gameData.find('blacktosave',0,firstMovePosition))
    tempSet.add(gameData.find('savetheblack',0,firstMovePosition))
    tempSet.add(gameData.find('rescuetheblack',0,firstMovePosition))
    tempSet.add(gameData.find('blacklive',0,firstMovePosition))
    tempSet.add(gameData.find('blacksave',0,firstMovePosition))
    tempSet.add(gameData.find('blacktorescue',0,firstMovePosition))
    tempSet.add(gameData.find('saveblack',0,firstMovePosition))
    tempSet.add(gameData.find('rescueblack',0,firstMovePosition))
    tempSet.add(gameData.find('keepblackalive',0,firstMovePosition))

    tempSet.remove(-1)
    if len(tempSet) > 0:
      setMinIndex = min(tempSet)
      if setMinIndex <= minIndex:
        self.problemType = 1
        minIndex = setMinIndex
    tempSet.clear()

    '''Black To Kill: 2'''
    tempSet.add(gameData.find('blacktokill',0,firstMovePosition))
    tempSet.add(gameData.find('blackkills',0,firstMovePosition))
    tempSet.add(gameData.find('blacktoplayandkill',0,firstMovePosition))
    tempSet.add(gameData.find('blackplaysandkills',0,firstMovePosition))
    tempSet.add(gameData.find('blacktotryandkill',0,firstMovePosition))
    tempSet.add(gameData.find('blacktoslaughterwhite',0,firstMovePosition))
    tempSet.add(gameData.find('blacktodohisbesttokill',0,firstMovePosition))
    tempSet.add(gameData.find('killthewhite',0,firstMovePosition))
    tempSet.add(gameData.find('blackkill',0,firstMovePosition))
    tempSet.add(gameData.find('blacktoattack',0,firstMovePosition))
    tempSet.add(gameData.find('blackattacks',0,firstMovePosition))
    tempSet.add(gameData.find('blackattack',0,firstMovePosition))
    tempSet.add(gameData.find('blacktofinish',0,firstMovePosition))
    tempSet.add(gameData.find('blackfinishs',0,firstMovePosition))
    tempSet.add(gameData.find('blackfinish',0,firstMovePosition))
    tempSet.add(gameData.find('blacktocapture',0,firstMovePosition))
    tempSet.add(gameData.find('blackcaptures',0,firstMovePosition))
    tempSet.add(gameData.find('blackcapture',0,firstMovePosition))
    tempSet.add(gameData.find('killwhite',0,firstMovePosition))
    tempSet.add(gameData.find('capturewhite',0,firstMovePosition))

    tempSet.remove(-1)
    if len(tempSet) > 0:
      setMinIndex = min(tempSet)
      if setMinIndex <= minIndex:
        self.problemType = 2
        minIndex = setMinIndex
    tempSet.clear()

    '''White To Live: 3'''
    tempSet.add(gameData.find('whitetolive',0,firstMovePosition))
    tempSet.add(gameData.find('whitelives',0,firstMovePosition))
    tempSet.add(gameData.find('whitetoplayandlive',0,firstMovePosition))
    tempSet.add(gameData.find('whiteplaysandlives',0,firstMovePosition))
    tempSet.add(gameData.find('whitetotryandlive',0,firstMovePosition))
    tempSet.add(gameData.find('whitetodohisbesttolive',0,firstMovePosition))
    tempSet.add(gameData.find('whitetoscrapeoutameagerexistence',0,firstMovePosition))
    tempSet.add(gameData.find('whitetosave',0,firstMovePosition))
    tempSet.add(gameData.find('savethewhite',0,firstMovePosition))
    tempSet.add(gameData.find('rescuethewhite',0,firstMovePosition))
    tempSet.add(gameData.find('whitelive',0,firstMovePosition))
    tempSet.add(gameData.find('whitesave',0,firstMovePosition))
    tempSet.add(gameData.find('whitetorescue',0,firstMovePosition))
    tempSet.add(gameData.find('savewhite',0,firstMovePosition))
    tempSet.add(gameData.find('rescuewhite',0,firstMovePosition))
    tempSet.add(gameData.find('keepwhitealive',0,firstMovePosition))

    tempSet.remove(-1)
    if len(tempSet) > 0:
      setMinIndex = min(tempSet)
      if setMinIndex <= minIndex:
        self.problemType = 3
        minIndex = setMinIndex
    tempSet.clear()

    '''White To Kill: 4'''
    tempSet.add(gameData.find('whitetokill',0,firstMovePosition))
    tempSet.add(gameData.find('whitekills',0,firstMovePosition))
    tempSet.add(gameData.find('whitetoplayandkill',0,firstMovePosition))
    tempSet.add(gameData.find('whiteplaysandkills',0,firstMovePosition))
    tempSet.add(gameData.find('whitetotryandkill',0,firstMovePosition))
    tempSet.add(gameData.find('whitetoslaughterblack',0,firstMovePosition))
    tempSet.add(gameData.find('whitetodohisbesttokill',0,firstMovePosition))
    tempSet.add(gameData.find('killtheblack',0,firstMovePosition))
    tempSet.add(gameData.find('whitekill',0,firstMovePosition))
    tempSet.add(gameData.find('whitetoattack',0,firstMovePosition))
    tempSet.add(gameData.find('whiteattacks',0,firstMovePosition))
    tempSet.add(gameData.find('whiteattack',0,firstMovePosition))
    tempSet.add(gameData.find('whitetofinish',0,firstMovePosition))
    tempSet.add(gameData.find('whitefinishs',0,firstMovePosition))
    tempSet.add(gameData.find('whitefinish',0,firstMovePosition))
    tempSet.add(gameData.find('whiteto capture',0,firstMovePosition))
    tempSet.add(gameData.find('whitecaptures',0,firstMovePosition))
    tempSet.add(gameData.find('whitecapture',0,firstMovePosition))
    tempSet.add(gameData.find('killblack',0,firstMovePosition))
    tempSet.add(gameData.find('captureblack',0,firstMovePosition))

    tempSet.remove(-1)
    if len(tempSet) > 0:
      setMinIndex = min(tempSet)
      if setMinIndex <= minIndex:
        self.problemType = 4
        minIndex = setMinIndex
    tempSet.clear()


  def computeBoardDimensions(self,gameData):
    counter = 0
    currentChar = ''

    xList = []
    yList = []

    whitePositionLocations = [m.start() for m in re.finditer('AW', gameData)]
    blackPositionLocations = [m.start() for m in re.finditer('AB', gameData)]

    stonePositions = whitePositionLocations + blackPositionLocations
    stonePositions.sort()

    for i in stonePositions:
      isBlack = False
      if i in blackPositionLocations:
        isBlack = not self.flipColors
      if i in whitePositionLocations:
        isBlack = self.flipColors
      counter = 0
      while(True):
        currentChar = gameData[i + counter + 2]
        if (currentChar != '['):
          break
        currentChar = gameData[i + counter + 3]
        y = ord(currentChar) - ord('a')
        yList.append(y)
        currentChar = gameData[i + counter + 4]
        x = ord(currentChar) - ord('a')
        xList.append(x)
        counter += 4

    solutionNodes = self.getSolutionNodes()
    for node in solutionNodes:
      moveString = self.getMove(node)
      if moveString==None or len(moveString)==0:
        raise Exception('Move string not found for node {}'.format(node))
      move = self.formatMove(moveString)
      xList.append(move['x'])
      yList.append(move['y'])

    incorrectNodes = self.getIncorrectNodes()
    for node in incorrectNodes:
      move = self.formatMove(self.getMove(node))
      xList.append(move['x'])
      yList.append(move['y'])

    self.boardDimensions['xMax'] = min(max(xList)+2,18) 
    self.boardDimensions['xMin'] = max(min(xList)-2,0)
    self.boardDimensions['yMax'] = min(max(yList)+2,18)
    self.boardDimensions['yMin'] = max(min(yList)-2,0)

  def parseStartState(self, gameData):
    boardSizeLocation = gameData.find("SZ")
    sizeString = ''
    counter = 0
    currentChar = gameData[boardSizeLocation + counter + 3]

    '''
    while(currentChar != ']'):
      sizeString += currentChar
      counter += 1
      currentChar = gameData[boardSizeLocation + counter + 3]

    if(sizeString.isdigit()):
      size = int(sizeString)
    else:
      size = 19
    '''

    currentBoard = Board(self.boardDimensions['xMax'] - self.boardDimensions['xMin'] + 1,self.boardDimensions['yMax'] - self.boardDimensions['yMin'] + 1)
    whitePositionLocations = [m.start() for m in re.finditer('AW', gameData)]
    blackPositionLocations = [m.start() for m in re.finditer('AB', gameData)]

    stonePositions = whitePositionLocations + blackPositionLocations
    stonePositions.sort()

    for i in stonePositions:
      isBlack = False
      if i in blackPositionLocations:
        isBlack = not self.flipColors
      if i in whitePositionLocations:
        isBlack = self.flipColors
      counter = 0
      while(True):
        currentChar = gameData[i + counter + 2]
        if (currentChar != '['):
          break
        currentChar = gameData[i + counter + 3]
        y = ord(currentChar) - ord('a') - self.boardDimensions['yMin']
        currentChar = gameData[i + counter + 4]
        x = ord(currentChar) - ord('a') - self.boardDimensions['xMin']
        if isBlack:
            currentBoard.black_stones.append((x,y))
        else:
            currentBoard.white_stones.append((x,y))
        #currentBoard.place_stone(x,y,isBlack)
        counter += 4
    return currentBoard
