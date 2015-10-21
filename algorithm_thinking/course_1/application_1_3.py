"""
DPA algorithm 2015/6/15
author: You-Hao Chang

"""

import application_1_1 as app1_1

def compute_out_degree(dograph):
    """
    computes the out-degrees for the nodes in the graph
    """
    outdegree_dict = dict()
    for node in dograph.keys():
        outdegree_dict[node] = len(dograph[node])

    return outdegree_dict

#print app1_1.CITATION_URL
citation_graph = app1_1.load_graph(app1_1.CITATION_URL)
out_degree_distribution = compute_out_degree(citation_graph)
total_nodes = len(out_degree_distribution.keys())

total_edges = 0
for edges in out_degree_distribution.values():
    total_edges += edges


print "We have " + str(total_nodes) + " nodes." #27770
print "The average out-degree is " + str(float(total_edges)/total_nodes) #~12.7

