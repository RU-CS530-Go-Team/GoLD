'''
Created on Nov 17, 2014

@author: JBlackmore
'''
from gold.features.Feature import Feature

class StoneCountFeature(Feature):
    '''
    classdocs
    '''
    def calculate_feature(self):
        blackdiff = float(len(self.move.black_stones)-len(self.start.black_stones))
        numBlackStart = float(len(self.start.black_stones))
        numWhiteStart = float(len(self.start.white_stones))
        numBlackMove = float(len(self.move.black_stones))
        numWhiteMove = float(len(self.move.white_stones))
        blackRatioStart = numBlackStart / (numBlackStart + numWhiteStart + 0.0001)
        blackRatioMove = numBlackMove / (numBlackMove + numWhiteMove + 0.0001)
        blackBoardRatioStart = numBlackStart / (self.start.x * self.start.y)
        whiteBoardRatioStart = numWhiteStart / (self.start.x * self.start.y)
        blackBoardRatioMove = numBlackMove / (self.move.x * self.move.y)
        whiteBoardRatioMove = numWhiteMove / (self.move.x * self.move.y)
        whitediff = float(len(self.move.white_stones)-len(self.start.white_stones))
        return [blackRatioMove, blackRatioMove - blackRatioStart, blackBoardRatioMove, whiteBoardRatioMove, blackBoardRatioMove - blackBoardRatioStart, whiteBoardRatioMove - whiteBoardRatioStart, numBlackMove, numWhiteMove, blackdiff - whitediff]
