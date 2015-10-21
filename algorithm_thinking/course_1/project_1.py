"""
Algorigthm thinking Project 1
2015/06/08

author: You-Hao Chang
"""

EX_GRAPH0 = {0: set([1, 2]), 
             1: set([]), 
             2: set([])}

EX_GRAPH1 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3]),
             3: set([0]),
             4: set([1]),
             5: set([2]),
             6: set([])}

EX_GRAPH2 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3, 7]),
             3: set([7]),
             4: set([1]),
             5: set([2]),
             6: set([]),
             7: set([3]),
             8: set([1, 2]),
             9: set([0, 3, 4, 5, 6, 7])}

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
    
    return indegree_dict
            
def in_degree_distribution(digraph):
    """
    computes the unnormalized distribution of the in-degrees of the graph
    """
    indegree_dict = compute_in_degrees(digraph)
    indegree_distribution = dict()
    for bin_indegree in indegree_dict.values():
        #bin_indegree = len(adjacent_nodes)
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

#print compute_in_degrees(EX_GRAPH1)
#print in_degree_distribution(EX_GRAPH1)
#print compute_out_degree(EX_GRAPH1)
