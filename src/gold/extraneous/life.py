from gold.models.board import StoneGrouper


def determineLife(board, color):
    if color:
        stones = board.black_stones
        other = board.white_stones
    else:
        stones = board.white_stones
        other = board.black_stones
    initial_groups = StoneGrouper(stones)
    connected_groups = StoneGrouper(stones, board)
    
    #Connect all of the empty squares (ignoring the other color)
    fill_board = [[0] * board.y] * board.x
    for (x, y) in stones:
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
            try:
                regions[y].append((x_i, y_i))
            except:
                regions[y] = [(x_i, y_i)]
                
    #Determine which are enclosed by whatever color we're working on
    enclosed_regions = []
    for current_group in connected_groups:
        max_X = max([x[0] for x in current_group]) +1
        max_Y = max([x[1] for x in current_group]) +1
        min_Y = min([x[0] for x in current_group]) -1
        min_Y = min([x[1] for x in current_group]) -1
        
        for current_region in regions:
            if all(x < max_X and x > min_X and y < max_Y and y > min_Y for x, y in current_region):
                enclosed_regions.append(current_region)
        
    #Removing the places taken up by the other color of stones stones
    for current_region in enclosed_regions:
        for check in other:
            if check in current_region:
                current_region.remove(other)
    
    
        
    
    
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
    liberties = calculate_liberties(board, chain)
    return sorted(liberties) == sorted(region)


def calculate_liberties(group, board):
        current_liberties = set()
        for current_x, current_y in group:
            moves = [(current_x - 1, current_y), (current_x + 1, current_y), (current_x, current_y - 1), (current_x, current_y + 1)]
            for cm in moves:
                if cm[0] < 0 or cm[0] >= board.x or cm[1] < 0 or cm[1] >= board.y:
                    continue
                elif not (cm in boardblack_stones or cm in board.white_stones):
                    current_liberties.add(cm)
        return list(current_liberties)
        