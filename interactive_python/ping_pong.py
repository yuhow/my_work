# Implementation of classic arcade game Pong

#import simplegui
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
#LEFT = False
#RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]        
    ball_vel = [random.randrange(120, 240) / 60.0, random.randrange(60, 180) / 60.0]
    #ball_vel = [240 / 60., 0]
    
    if direction == "RIGHT":
        ball_vel[0] = math.fabs(ball_vel[0])
        ball_vel[1] = -(math.fabs(ball_vel[1]))
    elif direction == "LEFT":
        ball_vel[0] = -(math.fabs(ball_vel[0]))
        ball_vel[1] = -(math.fabs(ball_vel[1]))        

# define event handlers
def new_game():
    global paddle1_point1, paddle1_point2, paddle1_point3, paddle1_point4
    global paddle2_point1, paddle2_point2, paddle2_point3, paddle2_point4
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    paddle1_point1 = [0, (HEIGHT - PAD_HEIGHT) / 2] 
    paddle1_point2 = [paddle1_point1[0] + PAD_WIDTH, paddle1_point1[1]] 
    paddle1_point3 = [paddle1_point2[0], paddle1_point2[1] + PAD_HEIGHT]
    paddle1_point4 = [paddle1_point3[0] - PAD_WIDTH, paddle1_point3[1]]

    paddle2_point1 = [WIDTH - PAD_WIDTH, (HEIGHT - PAD_HEIGHT) / 2]
    paddle2_point2 = [paddle2_point1[0] + PAD_WIDTH, paddle1_point2[1]] 
    paddle2_point3 = [paddle2_point2[0], paddle2_point2[1] + PAD_HEIGHT]
    paddle2_point4 = [paddle2_point3[0] - PAD_WIDTH, paddle2_point3[1]]

    paddle1_pos = [paddle1_point1, paddle1_point2, paddle1_point3, paddle1_point4]
    paddle2_pos = [paddle2_point1, paddle2_point2, paddle2_point3, paddle2_point4]

    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0]

    score1 = 0
    score2 = 0

    if random.randrange(0, 2) == 0:
        spawn_ball("RIGHT")
    else:
        spawn_ball("LEFT")
        
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
         
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # left and right gutters
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] > paddle1_pos[0][1] and ball_pos[1] < paddle1_pos[3][1]:
            ball_vel[0] = - ball_vel[0]
            #print ball_vel[0], ball_vel[1]
            #if math.fabs(ball_vel[0]) < 10000 and math.fabs(ball_vel[1]) < 240:
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
        else:
            score2 += 1
            spawn_ball("RIGHT")
           
    elif ball_pos[0] >= WIDTH - 1 - PAD_WIDTH - BALL_RADIUS:
        if ball_pos[1] > paddle2_pos[0][1] and ball_pos[1] < paddle2_pos[3][1]:
            ball_vel[0] = - ball_vel[0]   
            #if math.fabs(ball_vel[0]) < 10000 and math.fabs(ball_vel[1]) < 240:            
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1            
        else:
            score1 += 1
            spawn_ball("LEFT")            
    # top and bottom walls
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] >= HEIGHT - 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Yellow", "Yellow")
    
    # update paddle's vertical position, keep paddle on the screen
    # paddle1
    if paddle1_pos[0][1] + paddle1_vel[1] < 0:
        paddle1_pos[0][1] = 0
        paddle1_pos[1][1] = 0
        paddle1_pos[2][1] = PAD_HEIGHT - 1        
        paddle1_pos[3][1] = PAD_HEIGHT - 1   
    elif paddle1_pos[3][1] + paddle1_vel[1] > HEIGHT - 1:
        paddle1_pos[0][1] = HEIGHT - 1 - PAD_HEIGHT
        paddle1_pos[1][1] = HEIGHT - 1 - PAD_HEIGHT
        paddle1_pos[2][1] = HEIGHT - 1        
        paddle1_pos[3][1] = HEIGHT - 1
    else:        
        paddle1_pos[0][1] += paddle1_vel[1]
        paddle1_pos[1][1] += paddle1_vel[1]
        paddle1_pos[2][1] += paddle1_vel[1]
        paddle1_pos[3][1] += paddle1_vel[1]
    # paddle2
    if paddle2_pos[0][1] + paddle2_vel[1] < 0:
        paddle2_pos[0][1] = 0
        paddle2_pos[1][1] = 0
        paddle2_pos[2][1] = PAD_HEIGHT - 1        
        paddle2_pos[3][1] = PAD_HEIGHT - 1   
    elif paddle2_pos[3][1] + paddle2_vel[1] > HEIGHT - 1:
        paddle2_pos[0][1] = HEIGHT - 1 - PAD_HEIGHT
        paddle2_pos[1][1] = HEIGHT - 1 - PAD_HEIGHT
        paddle2_pos[2][1] = HEIGHT - 1        
        paddle2_pos[3][1] = HEIGHT - 1
    else:        
        paddle2_pos[0][1] += paddle2_vel[1]
        paddle2_pos[1][1] += paddle2_vel[1]
        paddle2_pos[2][1] += paddle2_vel[1]
        paddle2_pos[3][1] += paddle2_vel[1]                
        
    # draw paddles
    canvas.draw_polygon(paddle1_pos, 1, "White", "Red")
    canvas.draw_polygon(paddle2_pos, 1, "White", "Green")
 
    # draw scores
    canvas.draw_text(str(score1), [WIDTH * 1 / 4, 50], 40, "White")
    canvas.draw_text(str(score2), [WIDTH * 3 / 4, 50], 40, "White")    
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = -10
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 10
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = -10
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 10
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key==simplegui.KEY_MAP["w"] :
        paddle1_vel[1] = 0
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 0
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = 0
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
buttun = frame.add_button("Reset", new_game, 100)

# start frame
new_game()
frame.start()
