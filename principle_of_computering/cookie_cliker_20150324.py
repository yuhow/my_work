"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies   = 0.0
        self._current_cookies = 0.0
        self._current_time    = 0.0
        self._current_cps	    = 1.0
        self._cc_history      = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Current time is " + str(self._current_time) + ",\n" + \
               "         Current cookies are " + str(self._current_cookies) + ",\n" + \
               "         Current CPS is " + str(self._current_cps) + ",\n" + \
               "         Buy item " + str(self._cc_history[-1][1]) + ",\n" + \
               "         The cost of item is " + str(self._cc_history[-1][2]) + ",\n" + \
               "         Total cookies produced are " + str(self._total_cookies) + ".\n"
    
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        copy_history = self._cc_history[:]
        return copy_history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies <= self._current_cookies:
            return 0.0
        else:
            return math.ceil((cookies - self._current_cookies) / self._current_cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._current_time += time
            self._current_cookies += time * self._current_cps
            self._total_cookies += time * self._current_cps
        else:
            return None
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self._current_cookies:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._cc_history.append((self._current_time, item_name, cost, self._total_cookies))
        else:
            return None
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """    
    copy_build_info = build_info.clone()
    clicker_state = ClickerState()
    time_to_next_buy = 0.0
    
    while clicker_state.get_time() <= duration:          
        target_item = strategy(clicker_state.get_cookies(), clicker_state.get_cps(),\
                               clicker_state.get_history(), duration - clicker_state.get_time(),\
                               copy_build_info)        
        if not target_item:           
            time_to_next_buy = duration - clicker_state.get_time()                       
            break
        else:
            time_to_next_buy = clicker_state.time_until(copy_build_info.get_cost(target_item))
            
        if time_to_next_buy > duration - clicker_state.get_time():             
            break
        
        clicker_state.wait(time_to_next_buy)
        clicker_state.buy_item(target_item, copy_build_info.get_cost(target_item), copy_build_info.get_cps(target_item))
        copy_build_info.update_item(target_item)    
        
    if time_to_next_buy:
        clicker_state.wait(duration - clicker_state.get_time())
        
    return clicker_state


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """    
    Always buy the cheapest item you can afford in the time left.
    """
    cookies_in_the_time_left = cookies + time_left * cps
    cheapest_item = None
    cheapest_item_cost = float("inf")
        
    for item in build_info.build_items():
        tmp_cheapest_item_cost = build_info.get_cost(item)
        if cookies_in_the_time_left >= tmp_cheapest_item_cost and tmp_cheapest_item_cost < cheapest_item_cost:
            cheapest_item = item
            cheapest_item_cost = tmp_cheapest_item_cost        
       
    return cheapest_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    cookies_in_the_time_left = cookies + time_left * cps
    most_expensive_item = None
    most_expensive_item_cost = float("-inf")
        
    for item in build_info.build_items():
        tmp_most_expensive_item_cost = build_info.get_cost(item)
        if cookies_in_the_time_left >= tmp_most_expensive_item_cost and tmp_most_expensive_item_cost > most_expensive_item_cost:
            most_expensive_item = item
            most_expensive_item_cost = tmp_most_expensive_item_cost        
       
    return most_expensive_item   

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    cookies_in_the_time_left = cookies + time_left * cps
    
    highest_cp_item = None
    highest_cp = 0
    
    for item in build_info.build_items():
        tmp_highest_cp = build_info.get_cps(item) / build_info.get_cost(item)
        if cookies_in_the_time_left > build_info.get_cost(item) and tmp_highest_cp > highest_cp:
            highest_cp_item = item
            highest_cp = tmp_highest_cp
            
    return highest_cp_item
    
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15), time, strategy)
    #state = simulate_clicker(provided.BuildInfo(), time, strategy)    
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    #run_strategy("Cursor", SIM_TIME, strategy_none)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

