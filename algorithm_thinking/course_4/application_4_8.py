"""
Algorithm thinking application 4-8

data: 2015/07/30
Author: You-Hao Chang
"""

import alg_application4_provided as app4
import AT_project_4 as pj4
import application_4_7 as sol4_7
import random
import time

def check_spelling(checked_word, dist, word_list):
    """
    To iterates through word_list and returns the set of
    all words that are within edit distance dist of the string checked_word
    """
    diag_score = 2
    off_diag_score = 1
    dash_score = 0

    scoring_matrix = pj4.build_scoring_matrix(set('qazwsxedcrfvtgbyhnujmikolp'), diag_score, off_diag_score, dash_score)
    word_list = set(word_list)

    candidate_words = list()
    count = 0
    for word in word_list:
        if len(word) < len(checked_word) - dist or len(word) > len(checked_word) + dist:
            continue
        
        # number of operation = 2
        # 2 insertion
        passed = False
        for number in range(len(checked_word)):
            if checked_word[:number] in word and checked_word[number + 2:] in word:
                passed = True

        # 1 insertion
        passed = True
        for number in range(len(checked_word)):
            if checked_word[:number] not in word or checked_word[number + 1:] not in word:
                passed = False

        if not passed:
            continue
        count += 1
        
        if sol4_7.edit_distance(checked_word, word, scoring_matrix) <= dist:
            candidate_words.append(word)

    print count
    
    return set(candidate_words)


word_list = app4.read_words(app4.WORD_LIST_URL)
for dummy in range(5):
    start_time = time.time()
    #set_check_humble = check_spelling('humble', 1, word_list)
    set_check_firefly = check_spelling('firefly', 2, word_list)
    print time.time() - start_time

#print "Candidates of 'humble' wiht '1' edit distance is " + str(set_check_humble)
#print "Candidates of 'firefly' with '2' edit distance is " + str(set_check_firefly)
