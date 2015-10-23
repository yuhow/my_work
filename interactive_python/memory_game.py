# implementation of card game - Memory

#import simplegui
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random

list1 = range(0, 8)
list2 = range(0, 8)
list_total = list1 + list2
turns = 0

# helper function to initialize globals
def new_game():
    global state, exposed, turns
    state = 0
    random.shuffle(list_total)
    exposed = [False] * 16
    turns = 0
    label.set_text("Turns = "+str(turns))

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global list_total, exposed, state, card1, card2, turns

    if exposed[pos[0] / 50] == True:
        return None
    if state == 0:
        turns += 1
        state = 1
        card1 = pos[0] / 50
        exposed[card1] = True
    elif state == 1:
        state = 2
        card2 = pos[0] / 50
        exposed[card2] = True
    else:
        turns += 1
        state = 1
        if list_total[card1] == list_total[card2]:
            card1 = pos[0] / 50
            exposed[card1] = True
        else:            
            exposed[card1] = False
            exposed[card2] = False
            card1 = pos[0] / 50
            exposed[card1] = True
    label.set_text("Turns = "+str(turns))
            
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for num in range(0, len(list_total)):
#        canvas.draw_polygon([[0 + 50 * num, 0], [50 + 50 * num, 0], [50 + 50 * num, 100], [0 + 50 * num, 100]], 2, "White", "Green")
        canvas.draw_text(str(list_total[num]), [15 + 50 * num , 65], 40, "White")
        if exposed[num] == False:        
            canvas.draw_polygon([[0 + 50 * num, 0], [50 + 50 * num, 0], [50 + 50 * num, 100], [0 + 50 * num, 100]], 2, "White", "Green")
    


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
