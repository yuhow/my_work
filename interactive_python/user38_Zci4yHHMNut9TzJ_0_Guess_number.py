# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
"""
Game of "Guess the number"

Editor: You-Hao Chang
2014/10/02

"""

import simplegui
import random
import math

#global variable
secret_number = -1
min_value = 0
max_value = 100
remaining_guess = 0

# helper function to start and restart the game
def new_game(min_value, max_value):    
    # initialize global variables used in your code here
    global remaining_guess
    remaining_guess = int(math.ceil(math.log(max_value, 2)))
    
    print ""
    print "New game. Range is from ", min_value, " to ", max_value    
    print "Number of remaining guesses is ", remaining_guess
        
    global secret_number
    secret_number = random.randrange(min_value, max_value)

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global min_value, max_value
    min_value = 0
    max_value = 100
    new_game(min_value, max_value)

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global min_value, max_value
    min_value = 0
    max_value = 1000
    new_game(min_value, max_value)
    
def input_guess(guess):
    # main game logic goes here	
    global remaining_guess
    guess_number = int(guess)
    remaining_guess -= 1

    print ""    
    print "Guess was", guess_number
    print "Number of remaining guesses is", remaining_guess
    
    if remaining_guess <= 0:
        print "You ran out of guesses.  The number was ", secret_number
        new_game(min_value, max_value)
    else:    
        
        if guess_number < secret_number:
            print "Higher"
        elif guess_number > secret_number:
            print "Lower"
        else:
            print "Correct"
            print "Congratulations!!"
            new_game(min_value, max_value)
    
# create frame
frame = simplegui.create_frame("Guess the number", 400, 400)

# register event handlers for control elements and start frame
input_number = frame.add_input("Enter your guess", input_guess, 100)
frame.add_button("Range: 0 - 100", range100, 200)
frame.add_button("Range: 0 - 1000", range1000, 200)

frame.start()

# call new_game 
new_game(min_value,max_value)


# always remember to check your completed program against the grading rubric
