from array import array

class IllegalMove(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

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
        
    def board_spaces(self):
        state = []
        for i in range(self.x):
            row = array('c')
            for j in range(self.y):
                if (i,j) in self.white_stones:
                    row.append('w')
                elif (i,j) in self.black_stones:
                    row.append('b')
                else:
                    row.append('0')
            state.append(row)
        return state
    
    def place_stone(self, x, y, isblack):
        if x < 0 or x >= self.x or y < 0 or y >= self.y:
            raise IllegalMove("Out of the Bounds of the Go Board")
        elif (x, y) in self.white_stones or (x, y) in self.black_stones:
            raise IllegalMove("There is already a stone there")
        elif isblack:
            self.black_stones.append((x, y))
        else:
            self.white_stones.append((x, y))
        self.update(isblack)
    
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
            print liberties
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

