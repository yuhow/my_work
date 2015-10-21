"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100       # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    This function takes a current board and the next player to move.
    The function should play a game starting with the given player 
    by making random moves, alternating between players.
    The function should return when the game is over. The modified 
    board will contain the state of the game    
    """
    while (board.check_win() == None):        
        empty_square_list = board.get_empty_squares()

        random_square = empty_square_list[random.randrange(0, len(board.get_empty_squares()))]   
        board.move(random_square[0], random_square[1], player)
        player = provided.switch_player(player)
       
        
def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists) 
    with the same dimensions as the Tic-Tac-Toe board, a board
    from a completed game, and which player the machine player is. 
    The function should score the completed board and update 
    the scores grid.
    """
    if board.check_win() == provided.DRAW:
        return None
    
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if (board.square(row, col) == provided.EMPTY):
                continue;
            elif (board.square(row, col) == player):
                if (board.check_win() == player):
                    scores[row][col] += SCORE_CURRENT
                else:
                    scores[row][col] -= SCORE_CURRENT
            else:
                if (board.check_win() == player):
                    scores[row][col] -= SCORE_OTHER
                else:
                    scores[row][col] += SCORE_OTHER                    

                    
def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores. 
    The function should find all of the empty squares with 
    the maximum score and randomly return one of them as a 
    (row, column) tuple.
    """
    empty_square_list = board.get_empty_squares()

    highest_score = -NTRIALS * SCORE_CURRENT - 1
    for square in empty_square_list:        
        if scores[square[0]][square[1]] >= highest_score:
            highest_score = scores[square[0]][square[1]]

    square_list_highest_score = []
    for square in empty_square_list:
        if scores[square[0]][square[1]] == highest_score:
            square_list_highest_score.append(square)
            
    if len(square_list_highest_score) > 1:
        random_best_move = random.randrange(0, len(square_list_highest_score))
        return square_list_highest_score[random_best_move]
    else:
        return square_list_highest_score[0]

    
def mc_move(board, player, trials):
    """
    This function takes a current board, which player the 
    machine player is, and the number of trials to run.
    """
    mc_score_table = [[0 for dummy_col in range(board.get_dim())] 
                         for dummy_row in range(board.get_dim())]        

    for dummy_trial in range(trials):
        copy_board = board.clone()
        mc_trial(copy_board, player)
        mc_update_scores(mc_score_table, copy_board, player)        
    
    best_move = get_best_move(board, mc_score_table)       
    return best_move

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
