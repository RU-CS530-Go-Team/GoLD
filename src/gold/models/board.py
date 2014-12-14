from array import array
from copy import deepcopy
from random import randint

class IllegalMove(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

MAX_MOVE_HISTORY = 2
class Board:
    x = 0
    y = 0
    white_stones = None
    black_stones = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.white_stones = []
        self.black_stones = []
        self.prior_moves = []
        self.zobrist = self.init_zobrist()
        self.hashval = self.hash()
        
    def __str__(self):
        ans = ""
        for i in range(self.x):
            for q in range(self.y):
                if (i, q) in self.white_stones:
                    ans += "W"
                elif (i, q) in self.black_stones:
                    ans += "B"
                else:
                    ans += "-"
            ans += "\n"
        return ans
    
    def init_zobrist(self):
        hashboard = []
        for i in range(self.x * self.y):
            q = randint(0, (2 ** 50) - 1)
            w = randint(0, (2 ** 50) - 1)
            hashboard.append([q, w])
        return hashboard
    
    def randbin(self, d): 
        mx = (2 ** d) - 1 
        b = randint(0, mx)
        return b#[2:].rjust(d, '0') 
    
    def __hash__(self):
        return self.hash()
    
    def hash(self, old = 0):
        ans = old
        for i, v in sorted(self.black_stones):
            ans = ans ^ self.zobrist[(i) * (self.y) + v][0]
        for i, v in sorted(self.white_stones):
            ans = ans ^ self.zobrist[(i) * (self.y) + v][0]
        return ans 
    
    def __eq__(self, other):
        if other is None:
            return False
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        this_white = set(self.white_stones)
        other_white = set(other.white_stones)
        if this_white!=other_white:
            return False
        this_black = set(self.black_stones)
        other_black = set(other.black_stones)
        if this_black!=other_black:
            return False
        return True
        #return (self.__hash__().__eq__(other.__hash__()))

    def clone(self):
        new = Board(self.x, self.y)
        new.white_stones = [x for x in self.white_stones]
        new.black_stones = [x for x in self.black_stones]
        new.prior_moves = [x for x in self.prior_moves]
        return new

    def group_stones(self, isblack):
        if isblack:
            stones = [{x} for x in self.black_stones]
        else:
            stones = [{x} for x in self.white_stones]
        # union-find

    def is_ko(self, x, y, isblack):
        return self.hash() in self.prior_moves

    def alone(self, x, y, isblack):
        moves = [(x + 1, y), (x -1, y), (x, y + 1), (x, y - 1)]
        stones = self.black_stones if isblack else self.white_stones
        for cm in moves:
            if cm[0] < 0 or cm[0] >= self.x or cm[1] < 0 or cm[1] >= self.y:
                continue
            if cm in stones: return False
        return True

    def place_stone(self, x, y, isblack):
        old = (deepcopy(self.black_stones), deepcopy(self.white_stones), deepcopy(self.prior_moves))
        if x < 0 or x >= self.x or y < 0 or y >= self.y:
            raise IllegalMove("({},{}) is Out of the Bounds of the Go Board".format(x,y))
        elif (x, y) in self.white_stones or (x, y) in self.black_stones:
            raise IllegalMove("({},{}) There is already a stone there".format(x,y))
        elif isblack:
            self.black_stones.append((x, y))
        else:
            self.white_stones.append((x, y))
        self.update(isblack)
        stones = self.black_stones if isblack else self.white_stones
        if (x, y) not in stones:
            raise IllegalMove("Suicide is not allowed")
        elif self.is_ko(x, y, isblack):
            self.black_stones, self.white_stones, self.prior_moves = old
            raise IllegalMove("Ko")
        self.prior_moves.append(self.hashval)
        if len(self.prior_moves)>=MAX_MOVE_HISTORY:
            self.prior_moves = self.prior_moves[1:]
        self.hashval = self.hash()
        
    def update(self, isblack):
        if isblack:
            first = self.white_stones
            second = self.black_stones
        else:
            first = self.black_stones
            second = self.white_stones
        for stone_set in (first, second):
            if stone_set == first:
                first_prime = True
            else:
                first_prime = False
            completed_stones = []
            liberties = []
            for primary_stone in stone_set:
                if primary_stone in completed_stones: continue
                attached_stones = [primary_stone]
                free_spaces = set()
                for current_stone in attached_stones:
                    x = current_stone[0]
                    y = current_stone[1]
                    for new_row, new_column in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                        if new_row < 0 or new_row >= self.x or new_column < 0 or new_column >= self.y:
                            continue
                        elif (new_row, new_column) in attached_stones:
                            continue
                        elif (new_row, new_column) in stone_set:
                            attached_stones.append((new_row, new_column))
                        elif first_prime and (new_row, new_column) in second:
                            continue
                        elif not first_prime and (new_row, new_column) in first:
                            continue
                        else:
                            free_spaces.add((new_row, new_column))
                completed_stones.extend(attached_stones)
                liberties.extend([(x[0], x[1], len(free_spaces)) for x in attached_stones])
            #print liberties
            if first_prime:
                first = [(x, y) for x, y, z in liberties if z != 0]
                if isblack:
                    self.white_stones = first
                else:
                    self.black_stones = first
            else:
                second = [(x, y) for x, y, z in liberties if z != 0]
                if isblack:
                    self.black_stones = second
                else:
                    self.white_stones = second
'''
 Implements union-find to group adjacent stones
 of the same color into sets.
'''
class StoneGrouper():
    ''' Doesnt really need the board... could just have stones
    def __init__(self, board, isblack):
        self.board = board
        self.isblack = isblack
        if isblack:
            self.stones = board.black_stones
        else:
            self.stones = board.white_stones
        self.group_stones()
    '''

    ''' Doesnt really need the board... could just have stones  '''
    def __init__(self, stones, board=None):
        self.board = board
        self.stones = stones
        self.group_stones()

    def find(self, element):
        for subset in self.groups:
            if element in subset:
                return subset
        raise ValueError('{} not found'.format(element))

    def union(self, set1, set2):
        i = self.groups.index(set1)
        self.groups[i] = set1.union(set2)
        self.groups.remove(set2)

    def is_space_adjacent(self, spc1, spc2):
        x1 = spc1[0]
        y1 = spc1[1]
        x2 = spc2[0]
        y2 = spc2[1]
        if x1==x2:
            return abs(y2-y1)==1
        if y1==y2:
            return abs(x2-x1)==1
        if self.board is not None: #checks for diagonal connections, only does so if the board is in.
            if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
                group = self.board.black_stones if (x1, y1) in self.board.white_stones else self.board.white_stones
                return (x1, y2) not in group or (x2, y1) not in group
        return False

    def is_group_adjacent(self, set1, set2):
        for spc1 in set1:
            for spc2 in set2:
                if self.is_space_adjacent(spc1, spc2):
                    return True
        return False

    def group_stones(self):
        self.groups = [{x} for x in self.stones]
        for i in range(len(self.stones)):
            for j in range(i+1, len(self.stones)):
                group1 = self.find(self.stones[i])
                group2 = self.find(self.stones[j])
                if group1!=group2 and self.is_group_adjacent(group1, group2):
                    self.union(group1, group2)
