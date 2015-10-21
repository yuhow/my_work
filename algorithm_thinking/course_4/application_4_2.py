"""
Algorithm thinking application 4-2

data: 2015/07/30
Author: You-Hao
"""

import alg_application4_provided as app4
import AT_project_4 as pj4

scoring_matrix = app4.read_scoring_matrix(app4.PAM50_URL)

seq_PAX = app4.read_protein(app4.CONSENSUS_PAX_URL)
seq_human = 'HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEK-QQ'
seq_fruitfly = 'HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ'

seq_human_nodash = ''
seq_fruitfly_nodash = ''

for char in seq_human:
    if char != '-':
        seq_human_nodash = seq_human_nodash + char

for char in seq_fruitfly:
    if char != '-':
        seq_fruitfly_nodash = seq_fruitfly_nodash + char

print len(seq_human_nodash)
print len(seq_fruitfly_nodash)

# for human
alignment_matrix = pj4.compute_alignment_matrix(seq_human_nodash, seq_PAX, scoring_matrix, True)

score_human, align_human, align_PAX_1 = pj4.compute_global_alignment(seq_human_nodash, seq_PAX, scoring_matrix, alignment_matrix)
print score_human
print align_human
print align_PAX_1

match_human = 0
for ind in range(len(align_human)):
    if align_human[ind] == align_PAX_1[ind]:
        match_human += 1
        
print float(match_human) / len(align_human) * 100.

# for fruit fly
alignment_matrix = pj4.compute_alignment_matrix(seq_fruitfly_nodash, seq_PAX, scoring_matrix, True)

score_fruitfly, align_fruitfly, align_PAX_2 = pj4.compute_global_alignment(seq_fruitfly_nodash, seq_PAX, scoring_matrix, alignment_matrix)
print score_fruitfly
print align_fruitfly
print align_PAX_2

match_fruitfly = 0
for ind in range(len(align_fruitfly)):
    if align_fruitfly[ind] == align_PAX_2[ind]:
        match_fruitfly += 1
        
print float(match_fruitfly) / len(align_fruitfly) * 100.
