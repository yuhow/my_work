"""
Application 2-3
Author: You-Hao Chang
Date: 2015.6.28

"""

import random
import time

from alg_upa_trial import UPATrial as upat

import alg_application2_provided as aa2p
import project_2 as pj2
import matplotlib.pyplot as plt

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
    
def edges_in_undirected_graph(ugraph):
    """
    :param ugraph: input an undeirected graph
    :return: number of edges
    """
    number_edges = 0
    for node in ugraph.keys():
        for edge in ugraph[node]:
            if edge < node and node in ugraph[edge]:
                continue
            else:
                number_edges += 1

    return number_edges

def get_upa_graph(number_total_nodes, number_init_nodes):
    """
    extract a upa graph
    :param number_total_nodes: total n nodes
    :param number_init_nodes: a initial graph with m nodes
    :return: a dictionary of an upa graph
    """
    graph_pool = upat(number_init_nodes)
    output_graph = make_complete_graph(number_init_nodes)
    for new_node in range(number_init_nodes, number_total_nodes):
        neighbor_nodes = graph_pool.run_trial(number_init_nodes)
        output_graph[new_node] = neighbor_nodes
        for neighbor_node in neighbor_nodes:
            output_graph[neighbor_node].add(new_node)
    
    return output_graph

#graph of UPA
#upa_graph = get_upa_graph(1239, 5)
#print edges_in_undirected_graph(upa_graph)

#different attack
#start_time = time.time()
#print start_time
#attack_order_v1 = aa2p.targeted_order(upa_graph)
#print time.time() - start_time
#attack_order_v2 = aa2p.fast_targeted_order(upa_graph)

#running time
running_time_v1 = []
for num_nodes in range(10, 1000, 10):
    upa_graph = get_upa_graph(num_nodes, 5)
    start_time = time.time()
    attack_order_v1 = aa2p.targeted_order(upa_graph)
    running_time_v1.append(time.time() - start_time)

running_time_v2 = []
for num_nodes in range(10, 1000, 10):
    upa_graph = get_upa_graph(num_nodes, 5)
    start_time = time.time()
    attack_order_v2 = aa2p.fast_targeted_order(upa_graph)
    running_time_v2.append(time.time() - start_time)
    
#making comparison plots
fig, ax = plt.subplots()
x_vals = [idx for idx in range(10, 1000, 10)]
#print len(x_vals)

ax.plot(x_vals, running_time_v1, '-b', label = 'targeted order')
ax.plot(x_vals, running_time_v2, '-r', label = 'fast targeted order')

ax.legend(loc = 'upper left')
ax.set_title('Timing results (in desktop Python)')
ax.set_xlabel('number of total nodes')
ax.set_ylabel('running time [second]')

plt.show()
