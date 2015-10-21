"""
Algorithm thinking application 4-1

data: 2015/07/30
Author: You-Hao
"""

import alg_application4_provided as app4
import AT_project_4 as pj4

protein_human = app4.read_protein(app4.HUMAN_EYELESS_URL)
protein_fruitfly = app4.read_protein(app4.FRUITFLY_EYELESS_URL)
scoring_matrix = app4.read_scoring_matrix(app4.PAM50_URL)
alignment_matrix_4_1 = pj4.compute_alignment_matrix(protein_human, protein_fruitfly, scoring_matrix, False)

score_4_1, align_human_4_1, align_fruitfly_4_1 = pj4.compute_local_alignment(protein_human, protein_fruitfly, scoring_matrix, alignment_matrix_4_1)
print score_4_1
print align_human_4_1
print align_fruitfly_4_1
