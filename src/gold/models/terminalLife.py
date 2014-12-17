from gold.models.life import *
from gold.models.board import Board, IllegalMove
#from board import Board, IllegalMove
from copy import deepcopy

checked = {}

def findAliveGroups(board, color, maxdepth=10):
    if color:
        stones = board.black_stones
        other = board.white_stones
    else:
        stones = board.white_stones
        other = board.black_stones
    initial_groups = [list(x) for x in StoneGrouper(stones).groups]
    connected_groups = [list(x) for x in StoneGrouper(stones, board).groups]
    fill_board = []
    for i in range(board.x):
        temp = []
        for w in range(board.y):
            temp.append(0)
        fill_board.append(temp)
    for x, y in stones:
        fill_board[x][y] = 1
    start_color = 2
    for x_i, x in enumerate(fill_board):
        for y_i, y in enumerate(x):
            if y == 0:
                flood_fill(fill_board, (x_i, y_i), 0, start_color)
                start_color += 1
    #Split up the filled groups into something that we can easily parse
    regions = {}
    for x_i, x in enumerate(fill_board):
        for y_i, y in enumerate(x):
            if y == 0 or y == 1: continue
            try:
                regions[y].append((x_i, y_i))
            except:
                regions[y] = [(x_i, y_i)]
    #remove all places taken up by the other color of stones
    for current_region in regions:
        for check in other:
            if check in regions[current_region]:
                regions[current_region].remove(check)
    #Determine which are enclosed by whatever color we're working on
    groups = set()
    for current_group in connected_groups:
        max_X = max([x[0] for x in current_group]) +1
        max_Y = max([x[1] for x in current_group]) +1
        min_X = min([x[0] for x in current_group]) -1
        min_Y = min([x[1] for x in current_group]) -1

        for current_region in regions:
            if all(x < max_X and x > min_X and y < max_Y and y > min_Y for x, y in regions[current_region]):
                groups.add(tuple(current_group))

    ans = []
    for current_group in groups:
        current_group = list(current_group)
        if alive(current_group, board, color, 0, maxdepth):
            ans.append(current_group)
    return ans

def alive(current_group, board, color, depth, maxdepth=10):
    if (tuple(board.black_stones), tuple(board.white_stones), board.x, board.y, tuple(current_group)) in checked:
        #print "Redundant"
        return checked[(tuple(board.black_stones), tuple(board.white_stones), board.x, board.y, tuple(current_group))]
    #print "Doing this group"
    #print current_group
    live_groups = determineLife(board, color)
    #print live_groups
    if live_groups != []:
        #print live_groups
        for live_group in live_groups:
            if any(x in live_group for x in current_group):
                #print "Returning"
                #print board.black_stones
                #print board.white_stones
                checked[(tuple(board.black_stones), tuple(board.white_stones), board.x, board.y, tuple(current_group))] = True
                return True
        #return True
    if depth > maxdepth: return False
    max_X = max([x[0] for x in current_group]) +1
    max_Y = max([x[1] for x in current_group]) +1
    min_X = min([x[0] for x in current_group]) -1
    min_Y = min([x[1] for x in current_group]) -1
    ans = True
    for x in range(min_X, max_X):
        for y in range(min_Y, max_Y):
            #print "Doing %d %d" % (x, y)
            try:
                current_board = deepcopy(board)
                current_board.place_stone(x, y, not color)
                current_alive = False
                #print current_board
                #print x, y
                #raw_input()
                for x1 in range(min_X, max_X):
                    for y1 in range(min_Y, max_Y):
                        try:
                            current_board_2 = deepcopy(current_board)
                            current_board_2.place_stone(x1, y1, color)
                            #print current_board_2
                            #print depth
                            if alive(current_group, current_board_2, color, depth + 1, maxdepth):
                                #print "Alive"
                                #print current_board_2
                                #raw_input()
                                current_alive = True
                                break
                        except IllegalMove as inst:
                            continue
                    if current_alive: break
                if not current_alive: ans = False
                if not ans: break
            except IllegalMove as inst:
                #print type(inst)
                #print inst.args
                continue

        if not ans: break
    checked[(tuple(board.black_stones), tuple(board.white_stones), board.x, board.y, tuple(current_group))] = ans
    return ans

#temp_board = Board(4, 8)
#temp_board.black_stones = [(1, 0), (1, 1), (1, 2), (2, 0), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 4), (0, 6)]
#temp_board.white_stones = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (1, 4), (1, 5), (2, 5), (3, 5)]#, (0, 6), (0, 5)]
#print temp_board
#print findAliveGroups(temp_board, True)
#temp_board.black_stones = [(1, 0), (1, 1), (1, 2), (1, 3), (0, 3)]
#temp_board.white_stones = [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (1, 4), (0, 4)]
#print temp_board
#print findAliveGroups(temp_board, True)
