from life import *
from gold.models.board import Board, IllegalMove
from copy import deepcopy

def findAliveGroups(board, color):
    if color:
        stones = board.black_stones
        other = board.white_stones
    else:
        stones = board.white_stones
        other = board.black_stones
    initial_groups = [list(x) for x in StoneGrouper(stones).groups]
    connected_groups = [list(x) for x in StoneGrouper(stones, board).groups]
    ans = []
    for current_group in connected_groups:
        print current_group
        if alive(current_group, board, color, 0):
            ans.append(current_group)
    
    return ans

def alive(current_group, board, color, depth):
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
                return True
        #return True
    #if depth > 5: return False
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
                            if alive(current_group, current_board_2, color, depth + 1):
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
