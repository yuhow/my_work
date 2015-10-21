"""
Algorigthm thinking Project 1
2015/06/08

author: You-Hao Chang
"""

import urllib2
import matplotlib.pyplot as plt

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    #print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

def make_complete_graph(num_nodes):
    """
    return a complete graph with "num_nodes" nodes
    """
    if num_nodes <= 0:
        return dict()
    else:
        all_nodes_list = [node for node in range(num_nodes)]
        tmp_graph = dict()
        for node in range(num_nodes):
            adjacent_nodes_list = all_nodes_list[:]
            adjacent_nodes_list.remove(node)
            tmp_graph.update({node: set(adjacent_nodes_list)})
        return tmp_graph
    
def compute_in_degrees(digraph):
    """
    computes the in-degrees for the nodes in the graph
    """
    indegree_dict = dict()
    for node in digraph.keys():
        indegree_dict[node] = 0
    for head_set in digraph.values():
        for head_node in head_set:
            indegree_dict[head_node] += 1
    #for node in digraph.keys():
    #    indegree = 0
    #    for head_set in digraph.values():
    #        if node in head_set:
    #           indegree += 1
    #    indegree_dict.update({node: indegree})
    #    
    return indegree_dict
            
def in_degree_distribution(digraph):
    """
    computes the unnormalized distribution of the in-degrees of the graph
    """
    indegree_dict = compute_in_degrees(digraph)
    indegree_distribution = dict()
    for bin_indegree in indegree_dict.values():
        if bin_indegree in indegree_distribution.keys():
            indegree_distribution[bin_indegree] = indegree_distribution[bin_indegree] + 1
        else:
            indegree_distribution.update({bin_indegree: 1})

    return indegree_distribution

def normalization(distribution):
    """
    To return a normalized distribution of the in-degrees of the graph
    """
    total_sum = 0
    for number in distribution.values():
        total_sum += number
        
    for bin in distribution.keys():
        distribution[bin] = float(distribution[bin]) / total_sum

    return distribution


#citation_graph = load_graph(CITATION_URL)
#citation_distribution = in_degree_distribution(citation_graph)
#nor_citation_distribution = normalization(citation_distribution)
#print nor_citation_distribution
#
#fig, ax = plt.subplots()
#input_data = [[key, nor_citation_distribution[key]] for key in nor_citation_distribution.keys()]
#input_data.sort()
#
#input_x = [component[0] for component in input_data]
#input_y = [component[1] for component in input_data]
#
#ax.plot(input_x, input_y)
#ax.set_title('normalized distribution of citation')
#ax.set_xlabel('times for being citated')
#ax.set_ylabel('frequency')
#ax.set_xscale('log')
#ax.set_yscale('log')

#plt.show()