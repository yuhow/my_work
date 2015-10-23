"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle
    ########################################################
    # additional method
    def position_tile(self, value):
        """
        return the position of the specific tile
        """        
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == value:
                    return (row, col)
                
        assert False, "There is no " + str(value)
                
    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            #print direction
            if direction == "l":                
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row, target_col) != 0:
            return False
        for row in range(target_row + 1, self.get_height()):
            for col in range(0, self.get_width()):
                if (row, col) != self.current_position(row, col):
                    return False
        for col in range(target_col + 1, self.get_width()):
            if (target_row, col) != self.current_position(target_row, col):
                return False
        
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        answer_position = self.current_position(target_row, target_col)
        across_row_movement = target_row - answer_position[0]
        across_col_movement = target_col - answer_position[1]
        solved_string_path = ""       	
        
        # case 1: across_row_movement > 1
        # case 2: across_row_movement = 1
        # case 3: across_row_movement = 0
        if across_row_movement > 1:
            solved_string_path += "u"
            if across_col_movement >= 0:
                solved_string_path += "l" * across_col_movement
                solved_string_path += "u" * (across_row_movement - 1)
                solved_string_path += "rdlur" * across_col_movement
            #elif across_col_movement == 0:
            #    solved_string_path += "u" * (across_row_movement - 1)
            else:
                solved_string_path += "r" * (-across_col_movement)
                solved_string_path += "u" * (across_row_movement - 1)
                solved_string_path += "ldrul" * (-across_col_movement)
            solved_string_path += "lddru" * (across_row_movement - 1)
            solved_string_path += "ld"
        elif across_row_movement == 1:
            if across_col_movement > 0:
                solved_string_path += "l" * across_col_movement
                solved_string_path += "u" * across_row_movement
                solved_string_path += "rdlur" * (across_col_movement - 1)
                solved_string_path += "rdl"
            elif across_col_movement == 0:
                solved_string_path += "uld"
            else:
                solved_string_path += "u"
                solved_string_path += "r" * (-across_col_movement)
                solved_string_path += "ulldr" * (-across_col_movement - 1)
                solved_string_path += "ullddruld"
        elif across_row_movement == 0:
            solved_string_path += "l" * across_col_movement
            solved_string_path += "urrdl" * (across_col_movement - 1)
                
        self.update_puzzle(solved_string_path)
        return solved_string_path

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        solved_string_path = "ur"        
        
        if self.current_position(target_row, 0) == (target_row - 1, 0):
            solved_string_path += "r" * (self.get_width() - 2)
            self.update_puzzle(solved_string_path)
            return solved_string_path
        else:
            answer_position = self.current_position(target_row, 0)
            across_row_movement = target_row - 1 - answer_position[0]
            across_col_movement = 1 - answer_position[1]
            
            # case 1: across_row_movement > 1
            # case 2: across_row_movement = 1
            # case 3: across_row_movement = 0
            if across_row_movement > 1:
                solved_string_path += "u"
                if across_col_movement >= 0:
                    solved_string_path += "l" * across_col_movement
                    solved_string_path += "u" * (across_row_movement - 1)
                    solved_string_path += "rdlur" * across_col_movement
                #elif across_col_movement == 0:
                #    solved_string_path += "u" * (across_row_movement - 1)
                else:
                    solved_string_path += "r" * (-across_col_movement)
                    solved_string_path += "u" * (across_row_movement - 1)
                    solved_string_path += "ldrul" * (-across_col_movement)
                solved_string_path += "lddru" * (across_row_movement - 1)
                solved_string_path += "ld"
            elif across_row_movement == 1:
                if across_col_movement > 0:
                    solved_string_path += "u"
                    solved_string_path += "l" * across_col_movement
                    solved_string_path += "druld"
                elif across_col_movement == 0:
                    solved_string_path += "uld"
                else: 
                    solved_string_path += "u"
                    solved_string_path += "r" * (-across_col_movement)
                    solved_string_path += "dllur" * (-across_col_movement - 1)
                    solved_string_path += "dluld"
            elif across_row_movement == 0:
                if across_col_movement == 0:
                    solved_string_path += "l"
                else:
                    solved_string_path += "r" * (-across_col_movement)
                    solved_string_path += "ulldr" * (-across_col_movement - 1 )
                    solved_string_path += "ulld"
            solved_string_path += "ruldrdlurdluurddlur"
            solved_string_path += "r" * (self.get_width() - 2)
        
        #print solved_string_path
        self.update_puzzle(solved_string_path)
        return solved_string_path

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(0, target_col) != 0:
            return False
        if (1, target_col) != self.current_position(1, target_col):
            return False
        for row in range(2, self.get_height()):
            for col in range(0, self.get_width()):
                if (row, col) != self.current_position(row, col):
                    return False
        for col in range(target_col + 1, self.get_width()):
            if (0, col) != self.current_position(0, col):
                return False
            if (1, col) != self.current_position(1, col):
                return False
        
        return True    

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(1, target_col) != 0:
            return False        
        for row in range(2, self.get_height()):
            for col in range(0, self.get_width()):
                if (row, col) != self.current_position(row, col):
                    return False
        for col in range(target_col + 1, self.get_width()):
            if (0, col) != self.current_position(0, col):
                return False
            if (1, col) != self.current_position(1, col):
                return False
        
        return True                

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        solved_string_path = "ld"
        
        if self.current_position(0, target_col) == (0, target_col - 1):
            self.update_puzzle(solved_string_path)
            return solved_string_path
        else:
            answer_position = self.current_position(0, target_col)
            across_row_movement = 1 - answer_position[0]
            across_col_movement = target_col - 1 - answer_position[1]
            
            # case 1: across_row_movement = 1
            # case 2: across_row_movement = 0
            if across_row_movement == 1:
                if across_col_movement > 0:
                    solved_string_path += "u"
                    solved_string_path += "l" * across_col_movement
                    solved_string_path += "drrul" * (across_col_movement - 1)
                    solved_string_path += "druld"
                #else:
                #    solved_string_path += "uld"
            elif across_row_movement == 0:
                if across_col_movement > 0:
                    #print across_col_movement
                    solved_string_path += "l" * across_col_movement
                    solved_string_path += "urrdl" * (across_col_movement - 1)
                else:
                    solved_string_path += "uld"
                    
            solved_string_path += "urdlurrdluldrruld"
        
        #print solved_string_path
        self.update_puzzle(solved_string_path)
        return solved_string_path
    
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        answer_position = self.current_position(1, target_col)
        across_row_movement = 1 - answer_position[0]
        across_col_movement = target_col - answer_position[1]
        solved_string_path = ""
        
        # case 1: across_row_movement = 1
        # case 2: across_row_movement = 0
        if across_row_movement == 1:
            if across_col_movement > 0:
                solved_string_path += "l" * across_col_movement
                solved_string_path += "u" * across_row_movement
                solved_string_path += "rdlur" * (across_col_movement - 1)
                solved_string_path += "rdlur"
            if across_col_movement == 0:
                solved_string_path += "u"
        elif across_row_movement == 0:
            solved_string_path += "l" * across_col_movement
            solved_string_path += "urrdl" * (across_col_movement - 1)
            solved_string_path += "ur"
                
        self.update_puzzle(solved_string_path)
        return solved_string_path

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        solved_string_path = ""

        # if tile 3 locates at (0, 0) and tile 0 locats
        # at (1, 1), it's a dead end!        
        solved_string_path += "lu"
        self.update_puzzle(solved_string_path)
        
        loop_counter = 0
        while not self.row0_invariant(0):            
            solved_string_path += "rdlu"
            self.update_puzzle("rdlu")
            loop_counter += 1
            assert loop_counter <= 4, "It's a dead end..."

        return solved_string_path
    
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        #print self
        solved_string_path = ""
        
        # phase 0:
        if self.position_tile(0) != (self.get_height() - 1, self.get_width() - 1):
            across_row_movement = self.get_height() - 1 - self.position_tile(0)[0]
            across_col_movement = self.get_width() - 1 - self.position_tile(0)[1]
            solved_string_path += "d" * across_row_movement
            solved_string_path += "r" * across_col_movement
            
        self.update_puzzle(solved_string_path)
        
        #print "phase 1"
        # phase 1:
        while self.position_tile(0)[0] >= 2:
            #print "phase 1 start"
            self.lower_row_invariant(self.position_tile(0)[0], self.position_tile(0)[1])
            #print "interior"
            #print self
            solved_string_path += self.solve_interior_tile(self.position_tile(0)[0], self.position_tile(0)[1])
            self.lower_row_invariant(self.position_tile(0)[0],self.position_tile(0)[1])
            #print "col0"
            #print self
            if self.position_tile(0)[1] == 0:
                solved_string_path += self.solve_col0_tile(self.position_tile(0)[0])
            self.lower_row_invariant(self.position_tile(0)[0], self.position_tile(0)[1])
            #print self
            #print "done"
        
        #print "phase 2"
        # phase 2:
        while self.position_tile(0)[1] >= 2:
            #print "phase 2 start"
            #print "row1"
            #print self
            self.row1_invariant(self.position_tile(0)[1])
            solved_string_path += self.solve_row1_tile(self.position_tile(0)[1])
            #print "row0"
            #print self
            self.row0_invariant(self.position_tile(0)[1])
            solved_string_path += self.solve_row0_tile(self.position_tile(0)[1])
            self.row1_invariant(self.position_tile(0)[1])
            #print self

        #print "phase 3"
        # phase 3:
        #print "phase 3 start"
        #print self
        self.row1_invariant(self.position_tile(0)[1])
        solved_string_path += self.solve_2x2()
        #print self
        self.row0_invariant(self.position_tile(0)[1])
        
        return solved_string_path
            
# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(2, 2))
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 5, [[7, 6, 5, 3, 0], [4, 8, 2, 1, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]]))
#tmp_puzzle = Puzzle(3, 3, [[3,1,2],[4,8,7],[6,5,0]])
#tmp_puzzle.solve_interior_tile(2,2)
#print tmp_puzzle
#tmp_puzzle = Puzzle(4, 5, [[7, 6, 5, 3, 0], [4, 8, 2, 1, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#tmp_puzzle.solve_row0_tile(4)
#tmp_puzzle = Puzzle(2, 2, [[2,1],[3,0]])
#tmp_puzzle.solve_2x2()
#tmp_puzzle = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
#tmp_puzzle.solve_2x2()
#tmp_puzzle = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#tmp_puzzle = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#tmp_puzzle.solve_puzzle()
#tmp_puzzle.solve_interior_tile(2,2)
#print tmp_puzzle

