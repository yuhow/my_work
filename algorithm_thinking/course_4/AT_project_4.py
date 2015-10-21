"""
Algorithm thinking Project 4
Computing alignments of sequences

data: 2015/07/29
Author: You-Hao Chang
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    To builds a scoring matrix as a dictionary of dictionaries
    Input: alphabet, a set of characters
           dash_score, the score for any entry indexed by one or more dashes
           diag_score, the score for the remaining diagonal entries
           off_diag_score, the score for the remaining off-diagonal entries
    Output: a dictionary of dictionaries whose entries are indexed by pairs of
            characters in alphabet plus '-'
    """
    scroing_matrix = dict()
    complete_alphabet = alphabet.union('-')
    
    for row_char in complete_alphabet:
        scroing_matrix[row_char] = dict()        
        for col_char in complete_alphabet:
            if row_char != '-':
                if row_char == col_char:
                    scroing_matrix[row_char][col_char] = diag_score
                elif col_char != '-':
                    scroing_matrix[row_char][col_char] = off_diag_score
                else:
                    scroing_matrix[row_char][col_char] = dash_score
            else:
                scroing_matrix[row_char][col_char] = dash_score

    return scroing_matrix


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    To computes either a global alignment matrix or a local alignment matrix
    depending on the value of global_flag
    Input: seq_x and seq_y, two sequences
           scoring_matrix, a common alphabet with the scoring matrix
           global_flag, 'True' for a global alignment and 'False' for a local
                        alignment
    """
    length_x = len(seq_x)
    length_y = len(seq_y)
    alignment_matrix = [[float('-inf') for dummy_col in range(length_y + 1)] for dummy_row in range(length_x + 1)]
    alignment_matrix[0][0] = 0

    for ind_i in range(1, length_x + 1):
        alignment_matrix[ind_i][0] = alignment_matrix[ind_i - 1][0] + scoring_matrix[seq_x[ind_i - 1]]['-']
        if not global_flag and alignment_matrix[ind_i][0] < 0:
            alignment_matrix[ind_i][0] = 0
            
    for ind_j in range(1, length_y + 1):
        alignment_matrix[0][ind_j] = alignment_matrix[0][ind_j - 1] + scoring_matrix['-'][seq_y[ind_j - 1]]
        if not global_flag and alignment_matrix[0][ind_j] < 0:
            alignment_matrix[0][ind_j] = 0

    for ind_i in range(1, length_x + 1):
        for ind_j in range(1, length_y + 1):
            alignment_matrix[ind_i][ind_j] = max(alignment_matrix[ind_i - 1][ind_j - 1] + scoring_matrix[seq_x[ind_i - 1]][seq_y[ind_j - 1]],\
                                                 alignment_matrix[ind_i - 1][ind_j] + scoring_matrix[seq_x[ind_i - 1]]['-'],\
                                                 alignment_matrix[ind_i][ind_j - 1] + scoring_matrix['-'][seq_y[ind_j - 1]])
            if not global_flag and alignment_matrix[ind_i][ind_j] < 0:
                alignment_matrix[ind_i][ind_j] = 0

    return alignment_matrix


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    To compute global alignments of two sequences
    Input: seq_x and seq_y, two sequences
           scoring_matrix, scoring matrix
           alignment_matrix, global alignment matrix
    """
    ind_x = len(seq_x)
    ind_y = len(seq_y)
    align_x = ''
    align_y = ''

    while ind_x != 0 and ind_y != 0:
        if alignment_matrix[ind_x][ind_y] == alignment_matrix[ind_x - 1][ind_y - 1] + scoring_matrix[seq_x[ind_x - 1]][seq_y[ind_y - 1]]:
            align_x = seq_x[ind_x - 1] + align_x
            align_y = seq_y[ind_y - 1] + align_y
            ind_x -= 1
            ind_y -= 1
        else:
            if alignment_matrix[ind_x][ind_y] == alignment_matrix[ind_x - 1][ind_y] + scoring_matrix[seq_x[ind_x - 1]]['-']:
                align_x = seq_x[ind_x - 1] + align_x
                align_y = '-' + align_y
                ind_x -= 1
            else:
                align_x = '-' + align_x
                align_y = seq_y[ind_y - 1] + align_y
                ind_y -= 1

    while ind_x != 0:
        align_x = seq_x[ind_x - 1] + align_x
        align_y = '-' + align_y
        ind_x -= 1

    while ind_y != 0:
        align_x = '-' + align_x
        align_y = seq_y[ind_y - 1] + align_y
        ind_y -= 1

    return (alignment_matrix[len(seq_x)][len(seq_y)], align_x, align_y)


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    To compute local alignments of two sequences
    Input: seq_x and seq_y, two sequences
           scoring_matrix, scoring matrix
           alignment_matrix, local alignment matrix
    """    
    ind_x = -1
    ind_y = -1
    align_x = ''
    align_y = ''
    
    #find the maximum value over the entire matrix
    maximum = -1    
    for ind_row in range(0, len(seq_x) + 1):
        for ind_col in range(0, len(seq_y) + 1):
            if alignment_matrix[ind_row][ind_col] >= maximum:
                maximum = alignment_matrix[ind_row][ind_col]
                ind_x = ind_row
                ind_y = ind_col

    #tracback
    while ind_x != 0 and ind_y != 0:

        if alignment_matrix[ind_x][ind_y] <= 0:
            break
        
        if alignment_matrix[ind_x][ind_y] == alignment_matrix[ind_x - 1][ind_y - 1] + scoring_matrix[seq_x[ind_x - 1]][seq_y[ind_y - 1]]:
            align_x = seq_x[ind_x - 1] + align_x
            align_y = seq_y[ind_y - 1] + align_y
            ind_x -= 1
            ind_y -= 1
        else:
            if alignment_matrix[ind_x][ind_y] == alignment_matrix[ind_x - 1][ind_y] + scoring_matrix[seq_x[ind_x - 1]]['-']:
                align_x = seq_x[ind_x - 1] + align_x
                align_y = '-' + align_y
                ind_x -= 1
            else:
                align_x = '-' + align_x
                align_y = seq_y[ind_y - 1] + align_y
                ind_y -= 1

    #score
    score = 0
    for ind in range(len(align_x)):
        score += scoring_matrix[align_x[ind]][align_y[ind]]
        
    return (score, align_x, align_y)
