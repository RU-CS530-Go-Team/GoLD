'''
Created on Nov 22, 2014

@author: JGang
'''
from Feature import Feature

class DistanceFromCenterFeature(Feature):
    '''
    classdocs
    '''
    def calculate_feature(self):
        originalCenter = (sum([x[0] for x in self.start.black_stones + self.start.white_stones]) / (len(self.start.black_stones) + self.start.white_stones), sum([x[1] for x in self.start.black_stones + self.start.white_stones]) / (len(self.start.black_stones) + self.start.white_stones))
        furthest = max([((x[0] - orignalCenter[0]) ** 2 + (x[1] - originalCenter[1]) ** 2) ** .5 for x in self.start.black_moves + self.start.white_moves])
        #this shit can get replaced if we include what the move being considered is...
        black_move = filter(lambda x: x not in self.start.black_stones, self.move.black_stones)
        white_move = filter(lambda x: x not in self.start.white_stones, self.move.white_stones)
        if black_move == []:
            if white_move == []:
                raise Exception("Can't fiture out what the move is")
            else:
                return ((((white_move[0] - orignalCenter[0]) ** 2) + ((white_move[1] - originalCenter[1]) ** 2)) ** .5) / furthest
        else:
             return ((((black_move[0] - orignalCenter[0]) ** 2) + ((black_move[1] - originalCenter[1]) ** 2)) ** .5) / furthest
        
        
