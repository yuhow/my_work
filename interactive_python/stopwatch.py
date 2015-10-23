# template for "Stopwatch: The Game"
import simplegui

# define global variables
increment = 0
stop_attempt = 0
success_attempt = 0
is_time_running = False
position_try = [210, 30]
position_time = [100, 150]
time_interval = 100

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def stop_shot():    
    global stop_attempt, success_attempt
    # return composite string
    return str(success_attempt) + " / " + str(stop_attempt)

def format(t):    
    # A:BC.D for time format
    A = int(t / 600)    
    B = int((t - A * 600) / 100)
    C = int((t - A * 600 - B * 100) / 10)
    D = t - A * 600 - B * 100 - C * 10        
    
    # return composite string
    return str(A) + ":" + str(B) + str(C) + "." + str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global is_time_running
    timer.start()
    is_time_running = True

def stop():
    global is_time_running, increment, stop_attempt, success_attempt
    if is_time_running:
        stop_attempt += 1
        if increment % 10 == 0:
            success_attempt += 1
    timer.stop()
    is_time_running = False
    
def reset():  
    global increment, stop_attempt, success_attempt
    timer.stop()
    increment = 0
    stop_attempt = 0
    success_attempt = 0
    
# define event handler for timer with 0.1 sec interval
def tick():
    global increment
    increment += 1
    #print increment
    
# define draw handler
def draw(canvas):
    canvas.draw_text(stop_shot(), position_try, 30, "Yellow")
    canvas.draw_text(format(increment), position_time, 40, "White")
    
# create frame
frame = simplegui.create_frame("StopWatch", 300, 300)

# register event handlers
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(time_interval, tick)

# start frame
frame.start()

# Please remember to review the grading rubric
