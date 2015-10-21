import random
import matplotlib.pyplot as plt
import project_1 as pj1

def er_algorithm(node_number, prob):
    """
    :param node_number: number of nodes
    :param prob: probability
    :return: dictionary undirected graph which nodes are generated randomly
    """
    graph_idd = {}
    for node_i in xrange(node_number):
        value = []
        for node_j in xrange(node_number):
            if node_i != node_j:
                random_prob = random.random()
                if random_prob < prob:
                    value.append(node_j)
        graph_idd[node_i] = value
    return graph_idd


er_distribution = pj1.in_degree_distribution(er_algorithm(1000, 0.5))
nor_er_distribution = pj1.normalization(er_distribution)

fig, ax = plt.subplots()
input_data = [[key, nor_er_distribution[key]] for key in nor_er_distribution.keys()]
input_data.sort()

input_x = [component[0] for component in input_data]
input_y = [component[1] for component in input_data]

ax.plot(input_x, input_y)
ax.set_title('Distribution of ER algorithm (1000 nodes, prob is 0.5)')
#ax.set_xscale('log')
#ax.set_yscale('log')

plt.show()
