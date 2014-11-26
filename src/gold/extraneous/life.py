#from board import *
from gold.models.board import StoneGrouper


def determineLife(board, color):
    if color:
        stones = board.black_stones
        other = board.white_stones
    else:
        stones = board.white_stones
        other = board.black_stones
    initial_groups = [list(x) for x in StoneGrouper(stones).groups]
    connected_groups = [list(x) for x in StoneGrouper(stones, board).groups]
    #print initial_groups
    #print connected_groups
    
    #Connect all of the empty squares (ignoring the other color)
    fill_board = []
    for i in range(board.x):
        temp = []
        for w in range(board.y):
            temp.append(0)
        fill_board.append(temp)
    #fill_board = [[0] * board.y] * board.x
    #print fill_board
    for x, y in stones:
        fill_board[x][y] = 1
    #print fill_board
    start_color = 2
    for x_i, x in enumerate(fill_board):
        for y_i, y in enumerate(x):
            if y == 0:
                flood_fill(fill_board, (x_i, y_i), 0, start_color)
                start_color += 1
    #print fill_board
    #Split up the filled groups into something that we can easily parse
    regions = {}
    for x_i, x in enumerate(fill_board):
        for y_i, y in enumerate(x):
            if y == 0 or y == 1: continue
            try:
                regions[y].append((x_i, y_i))
            except:
                regions[y] = [(x_i, y_i)]
    #print regions
    #remove all places taken up by the other color of stones
    for current_region in regions:
        for check in other:
            if check in regions[current_region]:
                regions[current_region].remove(check)
    #print regions
    #Determine which are enclosed by whatever color we're working on
    enclosed_regions = []
    groups_by_region = {}
    for current_group in connected_groups:
        max_X = max([x[0] for x in current_group]) +1
        max_Y = max([x[1] for x in current_group]) +1
        min_X = min([x[0] for x in current_group]) -1
        min_Y = min([x[1] for x in current_group]) -1
        
        for current_region in regions:
            if all(x < max_X and x > min_X and y < max_Y and y > min_Y for x, y in regions[current_region]):
                enclosed_regions.append(regions[current_region])
                try:
                    groups_by_region[current_region].append(current_group)
                except:
                    groups_by_region[current_region] = [current_group]
    #print enclosed_regions
    #print groups_by_region
    #Starting Benson's Algorithm
    initial_groups = sorted(initial_groups)
    while(True):
        modified = False
        for chain in initial_groups:
            #print chain
            num_vital = 0
            for region in enclosed_regions:
                #print region
                if vital(chain, board, region):
                    num_vital += 1
                    #print "Is Vital"
                    #print chain, region
            if num_vital < 2:
                #print "Removing due to lack of vital areas"
                #print chain
                initial_groups.remove(chain)
                modified = True
        if not modified:
            break
        modified = False
        for region in groups_by_region.keys():
            cmodified = False    
            current_groups = groups_by_region[region]
            for each_group in current_groups:
                for each_stone in each_group:
                    if any(each_stone not in looking_at_group for looking_at_group in initial_groups):
                        modified = True
                        cmodified = True
                        #print "Getting rid of something"
                        #print region
                        #print groups_by_region
                        #print regions[region]
                        #print groups_by_region[region]
                        del groups_by_region[region]
                        #print enclosed_regions
                        enclosed_regions.remove(regions[region])
                        break
                if cmodified: break
        if not modified: break
                
                
    #print initial_groups
    return initial_groups
    
    
        
    
    
def flood_fill(fill_board, current_node, target_color, replacement_color):
    if target_color == replacement_color: return
    x, y = current_node
    if fill_board[x][y] != target_color: return
    fill_board[x][y] = replacement_color
    places = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for cm in places:
        if cm[0] < 0 or cm[0] >= len(fill_board) or cm[1] < 0 or cm[1] >= len(fill_board[0]):
            continue
        flood_fill(fill_board, cm, target_color, replacement_color)
    return

def vital(chain, board, region):
    
    liberties = calculate_liberties(chain, board)
    #print "In Vital"
    #print liberties
    #print region
    return all(x in liberties for x in region)


def calculate_liberties(group, board):
        current_liberties = set()
        for current_x, current_y in group:
            moves = [(current_x - 1, current_y), (current_x + 1, current_y), (current_x, current_y - 1), (current_x, current_y + 1)]
            for cm in moves:
                if cm[0] < 0 or cm[0] >= board.x or cm[1] < 0 or cm[1] >= board.y:
                    continue
                elif not (cm in board.black_stones or cm in board.white_stones):
                    current_liberties.add(cm)
        return list(current_liberties)
    
#test = Board(3, 5)
#test.black_stones = [(1, 0), (1, 1), (1, 2), (0, 1), (2, 4), (2, 3), (2, 2)]
#test.white_stones = [(1, 3)]
#print test
#determineLife(test, True)      