"""
Application 2-1
Author: You-Hao Chang
Date: 2015.6.28

"""

import random

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

def er_algorithm(node_number, prob):
    """
    :param node_number: number of nodes
    :param prob: probability
    :return: dictionary undirected graph which nodes are generated randomly
    """    
    ugraph = {node: set([]) for node in range(node_number)}
    for node_i in xrange(node_number):
        for node_j in xrange(node_number):
            if node_i != node_j:
                random_prob = random.random()
                if random_prob < prob:
                    ugraph[node_i].add(node_j)
                    ugraph[node_j].add(node_i)

    return ugraph

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

def random_order(ugraph):
    """
    :param ugraph: input an undisrected graph
    :return: a list of nodes in the graph in some random order
    """
    random_nodes_list = []
    for node in ugraph.keys():
        random_nodes_list.append(node)
    random.shuffle(random_nodes_list)

    return random_nodes_list

#graph of computer network
cn_graph = aa2p.load_graph(aa2p.NETWORK_URL)
print edges_in_undirected_graph(cn_graph)

#graph of ER
er_graph = er_algorithm(len(cn_graph.keys()), 0.002)
#print er_graph
print edges_in_undirected_graph(er_graph)

#graph of UPA
upa_graph = get_upa_graph(len(cn_graph.keys()), 2)
print edges_in_undirected_graph(upa_graph)

#random attack
cn_attack_order = random_order(cn_graph)
er_attack_order = random_order(er_graph)
upa_attack_order = random_order(upa_graph)

#resilience for different graphs
cn_resilience = pj2.compute_resilience(aa2p.copy_graph(cn_graph), cn_attack_order)
er_resilience = pj2.compute_resilience(aa2p.copy_graph(er_graph), er_attack_order)
upa_resilience = pj2.compute_resilience(aa2p.copy_graph(upa_graph), upa_attack_order)

#making comparison plots
fig, ax = plt.subplots()

print len(cn_resilience)
x_vals = [idx for idx in range(len(cn_graph.keys()) + 1)]
print len(x_vals)

ax.plot(x_vals, cn_resilience, '-b', label = 'computer network')
ax.plot(x_vals, er_resilience, '-r', label = 'ER graph (p = 0.002)')
ax.plot(x_vals, upa_resilience, '-g', label = 'UPA graph (m = 2)')
ax.legend(loc = 'upper right')
ax.set_title('Resiliences of different models ')
ax.set_xlabel('Number of removed nodes')
ax.set_ylabel('Value of largest connected component')
plt.show()
