#!/usr/bin/env python

import community
import networkx as nx
import matplotlib.pyplot as plt
import sys

#better with karate_graph() as defined in networkx example.
#erdos renyi don't have true community structure
#G = nx.erdos_renyi_graph(30, 0.05)

with open(sys.argv[1], "rb") as fp:
    G = nx.read_weighted_edgelist(fp)

#first compute the best partition
partition = community.best_partition(G)

#drawing
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0
for com in set(partition.values()) :
    count = count + 1
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    print("[{}]: {}".format(count, list_nodes))
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))

nx.draw_networkx_edges(G,pos, alpha=0.5)
plt.show()
