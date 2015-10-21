"""
Algorithm thinking application 4-7

data: 2015/07/30
Author: You-Hao Chang
"""

import AT_project_4 as pj4

def edit_distance(seq_x, seq_y, scoring_matrix):
    """
    calculate the edit distance through seq_x, seq_y and scoring matrix
    by return |seq_x| + |seq_y| - score of the corresponding global alignment
    """
    alignment_matrix = pj4.compute_alignment_matrix(seq_x, seq_y, scoring_matrix, True)
    score, align_x, align_y = pj4.compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
    return len(seq_x) + len(seq_y) - score

def ED_xcross_test(diag_score, off_diag_score, dash_score):
    """
    Insertion: abc -> abbc
    Deletion: abc -> ac
    Subsititution: abc -> abd
    """
    scoring_matrix = pj4.build_scoring_matrix({'a', 'b', 'c', 'd'}, diag_score, off_diag_score, dash_score)
    
    #test I: x = 'abcd', y = 'ad', the edit distance is 4
    test1_ED = edit_distance('ab', 'acccc', scoring_matrix)

    #test II: x = 'abc', y = 'abcddd', the edit distance is 3
    test2_ED = edit_distance('acccd', 'ad', scoring_matrix)

    #test III: x = 'abcd', y = 'abb', the edit distance is 2
    test3_ED = edit_distance('abcd', 'addd', scoring_matrix)

    return (test1_ED, test2_ED, test3_ED)

def find_optimal_scoring_matrix():
    """
    To determine the arguments of scoring matrix:
    diag_score, off_diag_score, dash_score
    """
    answer = (4, 3, 2)

    for diag_score in range(10):
        for off_diag_score in range(-10, 5):
            for dash_score in range(-10, 5):
                result = ED_xcross_test(diag_score, off_diag_score, dash_score)
                #print result
                if result == answer:
                    print "The optimal scoring matrix of ['a', 'b', 'c', 'd'] is with " +\
                          "diag_score = " + str(diag_score) +\
                          ", off_diag_score = " + str(off_diag_score) +\
                          " and dash_scor = " + str(dash_score)
    
    return None

find_optimal_scoring_matrix()

"""
optimal result:

diag_score = 2
off_diag_score = 1
dash_score = 0
"""
    
