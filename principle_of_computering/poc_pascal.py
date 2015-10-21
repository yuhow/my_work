"""
Iterative program to print out Pascal's triangle
"""

TRIANGLE_HEIGHT = 5

def next_line(current_line):
    """
    Given a line in Pascal's triangle, generate the following line
    """
    
    ans = [1]
    
    for idx in range(len(current_line) - 1):
        ans.append(current_line[idx] + current_line[idx + 1])
    
    ans.append(1)
    
    return ans

def run_example():
    # code to print out Pascal's triangle
    pascal_line = [1]	# row zero
    print pascal_line
    
    for dummy_idx in range(TRIANGLE_HEIGHT - 1):
        pascal_line = next_line(pascal_line)
        print pascal_line
        
run_example()
    
    