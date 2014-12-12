'''
Created on Dec 7, 2014

@author: JBlackmore
'''
import sys
import os
from glob import glob
from gold.extraneous.MoveTreeParser import MoveTreeParser
from gold.extraneous.life import determineLife
from gold.ui.Launcher import Launcher
from gold.extraneous.MoveTreeParser import UnspecifiedProblemType

def probfile_move_to_board_state(probfile, moveid):
    mtp= MoveTreeParser(probfile)
    ss = mtp.getAllPaths()
    move = mtp.start.clone()
    #print_move('start ({}x{})'.format(move.x, move.y), move)
    isBtL = (mtp.problemType == 1 or mtp.problemType==3)
    pt = 1 if isBtL else 2
    sw = len(determineLife(move, False))
    sb = len(determineLife(move, True))
    if sb>0:
        print('{}: Black is already alive!'.format(probfile))
    # prob type, solution, terminal, # living black groups, # living white groups
    #tpl= (pt, 1, 0, sb, sw)
    for spath in ss:
        move = mtp.start.clone()
        if moveid in spath:
            for step in spath:
                fm = mtp.formatMove(mtp.moveID[step])
                move.place_stone(fm['x'], fm['y'], fm['isBlack'])
                if step==moveid:
                    return move
    raise Exception('{}: Move id {} not found in problem file.'.format(probfile, moveid)) 

def get_moves_black_increasing_incorrect(probfile):
    mtp = MoveTreeParser(probfile)
    ss = mtp.getAllPaths()
    move = mtp.start.clone()
    #print_move('start ({}x{})'.format(move.x, move.y), move)
    isBtL = (mtp.problemType == 1 or mtp.problemType==3)
    pt = 1 if isBtL else 2
    sw = len(determineLife(move, False))
    sb = len(determineLife(move, True))
    if sb>0:
        print('{}: Black is already alive!'.format(probfile))
    problems = []
    # prob type, solution, terminal, # living black groups, # living white groups
    #tpl= (pt, 1, 0, sb, sw)
    for spath in ss:
        move = mtp.start.clone()
        for step in spath:
            fm = mtp.formatMove(mtp.moveID[step])
            move.place_stone(fm['x'], fm['y'], fm['isBlack'])
            w = len(determineLife(move, False))
            b = len(determineLife(move, True))
            sol = 1 if step in mtp.getSolutionNodes() else 0
            term = 1 if step in mtp.getTerminalStates() else 0
            bdiff = b-sb
            wdiff = w-sw    
            if bdiff>0 and sol==0:
                problems.append([step, fm['x'], fm['y'], fm['isBlack']])
    return problems

''' Who doesnt love depth-first search? '''
def file_search(search_dir):
    files = []
    for f in glob(search_dir+'/*'):
        if os.path.isdir(f):
            for sf in file_search(f):
                files.append(sf)
        elif f[-3:]=='sgf':
            files.append(f)
        else:
            print('Ignoring unrecognized file {}'.format(f.split('/')[-1]))
    return files


def view_problems(file_list):
    for f in file_list:
        if os.path.isdir(f):
            for f in file_search(f):
                try:
                    print(f)
                    bad_moves = get_moves_black_increasing_incorrect(f)
                    for bad_move in bad_moves:
                        [moveid, x, y, isblack] = bad_move
                        color = 'B' if isblack else 'W'
                        print('moveID {}={}({},{}): black groups increase (BtL), but on incorrect path'.format(moveid, color, x, y))
                        board = probfile_move_to_board_state(f, moveid)
                        ui = Launcher(400, 400, 50, max(board.x, board.y), board)
                        ui.drawBoard()
                        ui.mainloop()
                except UnspecifiedProblemType as upt:
                    error = upt
                    #print(error)
                    '''
                    except TypeError as te:
                        print(te)
                    '''
                except Exception as e:
                    print('Unexpected Error: {}'.format(e))

        else:
            try:
                bad_moves = get_moves_black_increasing_incorrect(f)
                for bad_move in bad_moves:
                    [moveid, x, y, isblack] = bad_move
                    board = probfile_move_to_board_state(f, moveid)
                    ui = Launcher(400, 400, 50, max(board.x, board.y), board)
                    ui.drawBoard()
                    ui.mainloop()
                '''
                except TypeError as te:
                    print(te)
                except UnspecifiedProblemType as upt:
                    error = upt
                    print(error)
                '''
            except Exception as e:
                print('Unexpected Error: {}'.format(e))

if __name__ == '__main__':
    if len(sys.argv)<2:
        print('Usage: python viewer.py <prob_file_or_dir>')
    probfiles = sys.argv[1:]
    view_problems(probfiles)
    