'''
Created on Nov 22, 2014

@author: JGang
'''
from Feature import Feature
from gold.models.board import StoneGrouper

class DiffLiberties(Feature):
    '''
    classdocs
    '''
    def calculate_feature(self):
        black_groups = [list(x) for x in StoneGrouper(self.start.black_stones).groups]
        black_liberties = self.calculate_liberties(black_groups)

        white_groups = [list(x) for x in StoneGrouper(self.start.white_stones).groups]
        white_liberties = self.calculate_liberties(white_groups)

        first_liberties_diff = black_liberties - white_liberties

        first_liberties_ratio = black_liberties / (black_liberties + white_liberties + 0.0001)

        first_libertiers_ratio_board_white = float(white_liberties) / (self.start.x * self.start.y)

        first_libertiers_ratio_board_black = float(black_liberties) / (self.start.x * self.start.y)

        black_groups = [list(x) for x in StoneGrouper(self.move.black_stones).groups]
        black_liberties = self.calculate_liberties(black_groups)

        white_groups = [list(x) for x in StoneGrouper(self.move.white_stones).groups]
        white_liberties = self.calculate_liberties(white_groups)

        second_liberties_diff = black_liberties - white_liberties

        second_liberties_ratio = black_liberties / (black_liberties + white_liberties + 0.0001)

        second_libertiers_ratio_board_white = float(white_liberties) / (self.move.x * self.move.y)

        second_libertiers_ratio_board_black = float(black_liberties) / (self.move.x * self.move.y)

        return [second_liberties_ratio, second_liberties_ratio - first_liberties_ratio, second_libertiers_ratio_board_black, second_libertiers_ratio_board_white, second_libertiers_ratio_board_black - first_libertiers_ratio_board_black, second_libertiers_ratio_board_white - first_libertiers_ratio_board_white, second_liberties_diff,  second_liberties_diff - first_liberties_diff, black_liberties, white_liberties]
    def calculate_liberties(self, groups):
        ans_libs = 0
        for group in groups:
            current_liberties = set()
            for current_x, current_y in group:
                moves = [(current_x - 1, current_y), (current_x + 1, current_y), (current_x, current_y - 1), (current_x, current_y + 1)]
                for cm in moves:
                    if cm[0] < 0 or cm[0] >= self.start.x or cm[1] < 0 or cm[1] >= self.start.y:
                        continue
                    elif not (cm in self.start.black_stones or cm in self.start.white_stones):
                        current_liberties.add(cm)
            ans_libs += len(current_liberties)
        return ans_libs
