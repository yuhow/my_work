"""
Algorithm thinking application 4-5

data: 2015/07/30
Author: You-Hao
"""

import math

def mean_value(scoring_distribution):
    """
    To caculate the mean of all scores
    """
    scores = scoring_distribution.keys()
    mean = sum([float(score * scoring_distribution[score]) for score in scores]) / sum(scoring_distribution.values())

    return mean


def std_deviation(scoring_distribution):
    """
    To calculate the standard deviation
    """
    n = len(scoring_distribution)
    scores = scoring_distribution.keys()
    mean = mean_value(scoring_distribution)
    
    variance = sum([scoring_distribution[score] * math.pow(score - mean, 2) for score in scores])
    standard_deviation = math.sqrt(variance / n)

    return standard_deviation


def z_score(alignment_score, scoring_distribution):
    """
    To calculate the z-score
    """
    mean = mean_value(scoring_distribution)
    standard_deviation = std_deviation(scoring_distribution)
    print "mean is " + str(mean)
    print "standard deviation is " + str(standard_deviation)

    return (alignment_score - mean) / standard_deviation

#v1
scoring_distribution = {38: 1, 39: 1, 40: 8, 41: 9, 42: 28, 43: 35, 44: 50, \
                        45: 46, 46: 49, 47: 57, 48: 63, 49: 62, 50: 72, \
                        51: 56, 52: 56, 53: 61, 54: 62, 55: 32, 56: 25, \
                        57: 33, 58: 29, 59: 22, 60: 25, 61: 15, 62: 13, \
                        63: 10, 64: 13, 65: 20, 66: 2, 67: 4, 68: 14, 69: 5, \
                        70: 3, 71: 2, 72: 3, 74: 2, 75: 2, 76: 1, 77: 1, \
                        79: 2, 81: 2, 84: 1, 85: 1, 94: 1, 97: 1}

#v2
#scoring_distribution = {39: 5, 40: 6, 41: 9, 42: 21, 43: 31, 44: 40, 45: 53, \
#                        46: 50, 47: 57, 48: 60, 49: 60, 50: 72, 51: 63, 52: \
#                        62, 53: 51, 54: 62, 55: 60, 56: 35, 57: 30, 58: 23, \
#                        59: 29, 60: 25, 61: 19, 62: 12, 63: 14, 64: 9, 65: 9, \
#                        66: 7, 67: 4, 68: 6, 69: 4, 70: 2, 71: 3, 72: 1, \
#                        73: 1, 74: 2, 75: 1, 80: 1, 95: 1}

print "z-score is " + str(z_score(875, scoring_distribution))
