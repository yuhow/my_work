"""
Application 3 of Algorithm thinking
2015/07/23

help functions

Author: You-Hao Chang
"""

import alg_cluster
import random

def gen_random_clusters(num_clusters):
    """
    creates a list of clusters where each cluster in this list
    corresponds to one randomly generated point in the square
    with corners (1,1), (1,-1), (-1, -1), (-1, 1)
    """
    cluster_list = []
    
    for dummy_idx in range(num_clusters):
        cluster_list.append(alg_cluster.Cluster(set([]), random.uniform(-1, 1), \
                                                random.uniform(-1, 1), 0, 0))

    return cluster_list

def compute_distortion(cluster_list, data_table):
    """
    compute the distortion of a clustering method
    """
    distortion = 0
    
    for cluster in cluster_list:
        distortion += cluster.cluster_error(data_table)

    return distortion
