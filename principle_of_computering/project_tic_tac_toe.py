"""
Mini-max Tic-Tac-Toe Player
"""

#import user39_lmN64yPcJ3_11 as poc_ttt_gui
#import poc_ttt_provided as provided
import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(120)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):    
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """    
    if board.check_win() != None:
        if board.check_win() == provided.PLAYERX:            
            
            return SCORES[provided.PLAYERX], (-1, -1)
        elif board.check_win() == provided.PLAYERO:                        
            return SCORES[provided.PLAYERO], (-1, -1)
        else:                       
            return SCORES[provided.DRAW], (-1, -1)
    else:                
        minimax_move = []
        for position in board.get_empty_squares():
            copy_board = board.clone()
            
            copy_board.move(position[0], position[1], player)
            copy_player = provided.switch_player(player)
                   
            temp_move = mm_move(copy_board, copy_player)
            temp_move = (temp_move[0], position)

            minimax_move.append(temp_move)
        
        if player == provided.PLAYERX:               
            maximizing = (-1,(-1,-1))
            for possible_move in minimax_move:
                if possible_move[0] > maximizing[0]:
                    maximizing = possible_move                
            return maximizing
        else:
            minimizing = (1,(-1,-1))
            for possible_move in minimax_move:
                if possible_move[0] < minimizing[0]:
                    minimizing = possible_move
            return minimizing


def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]    

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)