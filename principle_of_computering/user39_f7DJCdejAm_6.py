"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # slide the tiles before merging
    step1_list = [0] * len(line)
    for element in line:
        if element != 0:
            for index in range(len(step1_list)):
                if step1_list[index] == 0:
                    step1_list[index] = element
                    break    

    # merge
    step2_list = step1_list[0:]
    is_merged = False
    for index in range(len(step1_list)-1):
        if is_merged:
            is_merged = False
            continue           
        if step1_list[index] == step1_list[index + 1]:
            step2_list[index] = step1_list[index] * 2
            step2_list[index + 1]  =  0
            is_merged = True
                
    # slide tiles after merging
    step3_list = [0] * len(step2_list)
    for element in step2_list:
        if element != 0:
            for index in range(len(step3_list)):
                if step3_list[index] == 0:
                    step3_list[index] = element
                    break    
                
    return step3_list          

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width  = grid_width
        
        self._direction_dict = {UP:   [(0, col) for col in range(self._grid_width)],
                               DOWN: [(self._grid_height - 1 , col) for col in range(self._grid_width)],
                               LEFT: [(row, 0) for row in range(self._grid_height)],
                               RIGHT:[(row, self._grid_width - 1) for row in range(self._grid_height)]}
        self._grid = []
        self.reset()
        #print self.__str__()
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # initialize the grid
        self._grid = [[0 for dummy_col in range(self._grid_width)]
                        for dummy_row in range(self._grid_height)]        

        # random input for two tiles
        new_tile_counter = 0
        while new_tile_counter < 2:
            if (self.new_tile()):
                new_tile_counter += 1                        
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """        
        return str(self._direction_dict)

    def get_grid_height(self):
        """
        Get the height of the board.
        """        
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """        
        unchanged = True
        for initial_tile in self._direction_dict[direction]:                   
            if direction == 1 or direction == 2:
                tmp_list = self.transverse_tiles(initial_tile, OFFSETS[direction], self._grid_height)               
                merged_list = merge(tmp_list)
                
                if merged_list != tmp_list:
                    unchanged = False
                    
                for step in range(self._grid_height):
                    row = initial_tile[0] + step * OFFSETS[direction][0]
                    col = initial_tile[1] + step * OFFSETS[direction][1]
                    self.set_tile(row, col, merged_list[step])
                    
            elif direction == 3 or direction == 4:
                tmp_list = self.transverse_tiles(initial_tile, OFFSETS[direction], self._grid_width)
                merged_list = merge(tmp_list)
                
                if merged_list != tmp_list:
                    unchanged = False
                    
                for step in range(self._grid_width):
                    row = initial_tile[0] + step * OFFSETS[direction][0]
                    col = initial_tile[1] + step * OFFSETS[direction][1]
                    self.set_tile(row, col, merged_list[step])
                    
        if unchanged == False:
            new_tile_counter = 0
            while new_tile_counter < 1:
                if (self.new_tile()):
                    new_tile_counter += 1            

    def transverse_tiles(self, start_tile, direction_tuple, num_steps):
        """
        Function that iterates through the tiles in a grid
        in a linear direction
        
        Both start_tile is a tuple(row, col) denoting the
        starting tile
        
        direction is a tuple that contains difference between
        consecutive tiles in the traversal
        """        
        output_list = []
        for step in range(num_steps):
            row = start_tile[0] + step * direction_tuple[0]
            col = start_tile[1] + step * direction_tuple[1]
            output_list.append(self._grid[row][col])                
        return output_list    
    
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        row = random.randrange(0, self._grid_height)
        col = random.randrange(0, self._grid_width)
            
        if self._grid[row][col] == 0:
            if random.randint(0, 10) != 0:
                self.set_tile(row, col, 2)
                return True
            else:
                self.set_tile(row, col, 4)
                return True      
        return False
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value               

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """      
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(5, 4))