"""
Algorithm BFS-Visited, and an algorithm for computing the set of all 
connected components of a graph based on it, Algorithm CC-Visited.

Author: You-Hao Chang
Date: 2015.06.23

"""

from collections import deque

def bfs_visited(ugraph, start_node):
    """
    parameter:
        ugraph: input the undirected graph 
        start_node: input the start node
    output:
        the set consisting of all nodes that are 
        visited by a breadth-first search that 
        starts at start_node
    """
    queue_pool = deque()
    visited_nodes = set([start_node])
    queue_pool.append(start_node)
    while len(queue_pool):
        node = queue_pool.pop()
        for neighbor in ugraph[node]:
            if neighbor not in visited_nodes:
                visited_nodes.add(neighbor)
                queue_pool.append(neighbor)

    return visited_nodes

def cc_visited(ugraph):
    """
    parameter:
        ugraph: input the undirected graph
    output:
        a list of sets, where each set consists 
        of all the nodes in a connected component, 
        and there is exactly one set in the list 
        for each connected component in ugraph.
    """
    remaining_nodes = set(ugraph.keys())
    cc_sets = []
    while len(remaining_nodes):
        start_node = remaining_nodes.pop()
        visted_nodes = bfs_visited(ugraph, start_node)
        cc_sets.append(visted_nodes)
        remaining_nodes = remaining_nodes - visted_nodes

    return cc_sets

def largest_cc_size(ugraph):
    """
    parameter:
        ugraph: input the undirected graph
    output:
        the size (an integer) of the largest connected 
        component in ugraph
    """
    largest_cc = 0
    cc_sets = cc_visited(ugraph)
    for cc_set in cc_sets:
        if len(cc_set) > largest_cc:
            largest_cc = len(cc_set)

    return largest_cc

def compute_resilience(ugraph, attack_order):
    """
    subject a model of one particular network to random 
    and targeted "attacks".
    parameter:
        ugraph: input the undirected graph
        attack_order: a list of nodes
    """
    list_largest_cc_size = [largest_cc_size(ugraph)]
    for node in attack_order:
        ugraph.pop(node)
        for node_key in ugraph.keys():
            ugraph[node_key] = ugraph[node_key] - {node}
        list_largest_cc_size.append(largest_cc_size(ugraph))

    return list_largest_cc_size

