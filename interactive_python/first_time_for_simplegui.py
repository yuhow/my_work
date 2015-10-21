# SimpleGUI program template

# Import the module
import simplegui

# Define global variables (program state)
number_of_apple = 0
message = 'Hello...'

# Define "helper" functions
def increment_apple():    
    global number_of_apple
    number_of_apple += 1
 
# Define event handler functions
def tick():
    increment_apple()
    global message
    message = str(number_of_apple)+' apple(s)'
    print message
    
def click():
    timer.start()
    print 'I want to eat...'
    
def click_stop():
    timer.stop()

# Create a frame
frame = simplegui.create_frame("for test", 200, 200)

# Register event handlers
timer = simplegui.create_timer(1000,tick)
frame.add_button("I want to eat...", click)
frame.add_button("stop!", click_stop)

# Start frame and timers
frame.start()

