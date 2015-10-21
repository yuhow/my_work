"""
Application 3 of Algorithm thinking
2015/07/23

Question 3-10
Author: You-Hao Chang
"""

import math
import random
import urllib2
import alg_cluster
import AT_project_3 as pj3
import matplotlib.pyplot as plt

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]
                

def compute_distortion(cluster_list, data_table):
    """
    compute the distortion of a clustering method
    """
    distortion = 0
    
    for cluster in cluster_list:
        distortion += cluster.cluster_error(data_table)

    return distortion


data_table = load_data_table(DATA_896_URL)

#hierarchical_clustering
distortion_hc = []
for num_cluster in range(6, 21):
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

    cluster_list = pj3.hierarchical_clustering(singleton_list, num_cluster)
    distortion_hc.append(compute_distortion(cluster_list, data_table))
    print "Distortion of hierarchical clusters is ", str(compute_distortion(cluster_list, data_table))
    print "Displaying", len(cluster_list), "hierarchical clusters"

#kmeans_clustering
distortion_kc = []
for num_cluster in range(6, 21):
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
    cluster_list = pj3.kmeans_clustering(singleton_list, num_cluster, 5)
    distortion_kc.append(compute_distortion(cluster_list, data_table))
    print "Distortion of k-means clusters is ", str(compute_distortion(cluster_list, data_table))
    print "Displaying", len(cluster_list), "k-means clusters"

#making comparison plots
fig, ax = plt.subplots()
x_vals = [idx for idx in range(6, 21)]

ax.plot(x_vals, distortion_hc, '-b', label = 'hierarchical clustering')
ax.plot(x_vals, distortion_kc, '-r', label = 'kmeans clustering')

ax.legend(loc = 'upper right')
ax.set_title('Distortion results (896 counties) (in desktop Python)')
ax.set_xlabel('number of output clusters')
ax.set_ylabel('distortion')

plt.show()
