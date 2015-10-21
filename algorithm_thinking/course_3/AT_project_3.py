"""
Algorithm thinking HW3: Closest pairs and clustering algorithms 
2015/07/21
Author: You-Hao Chang
"""

import alg_cluster
import math
import random

def slow_closest_pair(cluster_list):
    """
    Ihe brute-force closest pair method
    Input: cluster_list, a list of 'Cluster' objects
    Outpur: a closest pair where the pair is represented by the tuple
    """
    closest_pair = [float('inf'), -1, -1]
    
    for idx1 in range(0, len(cluster_list)):
        for idx2 in range(idx1 + 1, len(cluster_list)):
            if cluster_list[idx1].distance(cluster_list[idx2]) <= closest_pair[0]:
                closest_pair = [cluster_list[idx1].distance(cluster_list[idx2]), idx1, idx2]
            idx2 += 1
        idx1 += 1

    # just in case...
    if closest_pair[1] > closest_pair[2]:
        closest_pair[1], closest_pair[2] = closest_pair[2], closest_pair[1]
        
    return tuple(closest_pair)
        

def fast_closest_pair(cluster_list):
    """
    The divide-and-conquer closest pair method
    Input: cluster_list, a list of 'Cluster' objects
    Output: a closest pair where the pair is represented by the tuple
    """
    cluster_list.sort(key = lambda cluster: cluster.horiz_center())
    
    closest_pair = [float('inf'), -1, -1]

    if len(cluster_list) <= 3:
        closest_pair = list(slow_closest_pair(cluster_list))
    else:
        half = len(cluster_list) / 2
        left_cl = cluster_list[:half]
        right_cl = cluster_list[half:]
        left_cp = list(fast_closest_pair(left_cl))
        right_cp = list(fast_closest_pair(right_cl))
        right_cp[1] = right_cp[1] + half
        right_cp[2] = right_cp[2] + half
        if left_cp[0] <= right_cp[0]:
            closest_pair = left_cp
        else:
            closest_pair = right_cp
        mid = (cluster_list[half - 1].horiz_center() + cluster_list[half].horiz_center()) / 2
        mid_cp = list(closest_pair_strip(cluster_list, mid, closest_pair[0]))
        if mid_cp[0] < closest_pair[0]:
            closest_pair = mid_cp            

    # just in case...
    if closest_pair[1] > closest_pair[2]:
        closest_pair[1], closest_pair[2] = closest_pair[2], closest_pair[1]
        
    return tuple(closest_pair)


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    The helper function of fast_closest_pair. It tries to find the
    closest pair of clusters that lie in the specified strip.
    Input: cluster_list, a list of 'Cluster' objects
           horiz_center,  the horizontal position of the center line for a vertical strip
           half_width, the maximal distance of any point in the strip from the center line.
    Output: a tuple corresponding to the closest pair of clusters that lie in the specified strip
    """
    # Build a hash table for original cluster_list, (x, y): idx
    hash_cl = {}
    for idx in range(len(cluster_list)):
        cluster = cluster_list[idx]
        hash_cl[(cluster.horiz_center(), cluster.vert_center())] = idx
    
    strip_cl = list()
    
    for cluster in cluster_list:
        if math.fabs(cluster.horiz_center() - horiz_center) <= half_width:
            strip_cl.append(cluster)

    strip_cl.sort(key = lambda cluster: cluster.vert_center())
    
    len_strip_cl = len(strip_cl)
    closest_pair = [float('inf'), -1, -1]
    
    for idx1 in range(len_strip_cl - 1):
        for idx2 in range(idx1 + 1, min(idx1 + 3, len_strip_cl - 1) + 1):
            distance_in_pair = strip_cl[idx1].distance(strip_cl[idx2])            
            if distance_in_pair < closest_pair[0]:
                cluster1_pos = (strip_cl[idx1].horiz_center(), strip_cl[idx1].vert_center())
                cluster2_pos = (strip_cl[idx2].horiz_center(), strip_cl[idx2].vert_center())
                closest_pair = [distance_in_pair, hash_cl[cluster1_pos], hash_cl[cluster2_pos]]

    # just in case...
    if closest_pair[1] > closest_pair[2]:
        closest_pair[1], closest_pair[2] = closest_pair[2], closest_pair[1]

    return tuple(closest_pair)


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Hierarchical clustering method
    Input: cluster_list, a list of 'Cluster' objects
           num_clusters, this clustering process should proceed
                         until 'num_clusters clusters' remain.
    Output: a new list of clusters
    """
    len_cl = len(cluster_list)
    while len_cl > num_clusters:
        closest_pair = fast_closest_pair(cluster_list)
        #closest_pair = slow_closest_pair(cluster_list)
        cluster_list[closest_pair[1]].merge_clusters(cluster_list[closest_pair[2]])
        cluster_list.remove(cluster_list[closest_pair[2]])
        len_cl = len(cluster_list)

    return cluster_list


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    K means clustering method
    Input: cluster_list, a list of 'Cluster' objects
           num_clusters, this clustering process should proceed
                         until 'num_clusters clusters' remain.
           num_iterations, the function should then compute 'num_iterations'
                           of k-means clustering
    Output: a new list of clusters
    """    
    len_cl = len(cluster_list)
    output_cluster_list = cluster_list[:]

    initial_centers = sorted(cluster_list, key = lambda cluster: cluster.total_population(), \
                             reverse = True)[:num_clusters]

    for dummy_iter in range(num_iterations):
        output_cluster_list = [alg_cluster.Cluster(set([]), 0, 0, 0, 0) for dummy_idx in range(num_clusters)]

        for idx_cluster in range(len_cl):
            closest_center = -1
            shortest_dist = float('inf')
            for idx_center in range(num_clusters):
                dist = cluster_list[idx_cluster].distance(initial_centers[idx_center])
                if dist < shortest_dist:
                    closest_center = idx_center
                    shortest_dist = dist

            output_cluster_list[closest_center].merge_clusters(cluster_list[idx_cluster])

        for idx in range(num_clusters):
            initial_centers[idx] = output_cluster_list[idx]
        
    return output_cluster_list
    
    
