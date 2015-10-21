"""
Application 1-4
author: You-Hao Chang
2015/06/15
"""

from dpa_algorithm import DPATrial as dpat
import project_1 as pj1
import matplotlib.pyplot as plt


def get_dpa_graph(number_total_nodes, number_init_nodes):
    """
    extract a dpa graph
    :param number_total_nodes: total n nodes
    :param number_init_nodes: a initial graph with m nodes
    :return: a dictionary of a dpa graph
    """
    graph_pool = dpat(number_init_nodes)
    output_graph = pj1.make_complete_graph(number_init_nodes)
    for new_node in range(number_init_nodes, number_total_nodes):
        neighbor_nodes = graph_pool.run_trial(number_init_nodes)
        output_graph[new_node] = neighbor_nodes
    
    return output_graph

dpa_graph = get_dpa_graph(27770, 13)
id_distribution_dpa = pj1.in_degree_distribution(dpa_graph)

nor_id_distribution_dpa = pj1.normalization(id_distribution_dpa)
#print nor_citation_distribution

fig, ax = plt.subplots()
input_data = [[key, nor_id_distribution_dpa[key]] for key in nor_id_distribution_dpa.keys()]
input_data.sort()

input_x = [component[0] for component in input_data]
input_y = [component[1] for component in input_data]

ax.plot(input_x, input_y)
ax.set_title('normalized distribution of DPA')
ax.set_xscale('log')
ax.set_yscale('log')

plt.show()
