#!/usr/bin/env python

import click
import community
import json
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pformat
import sys
import gids2names

#better with karate_graph() as defined in networkx example.
#erdos renyi don't have true community structure
#G = nx.erdos_renyi_graph(30, 0.05)

dflt_resolution = 0.5

def gen_clusters(edges_file, resolution=dflt_resolution):
    with open(edges_file, "rb") as fp:
        G = nx.read_weighted_edgelist(fp)

    dendrogram = community.generate_dendrogram(G, resolution=0.25)
    len_d = len(dendrogram)
    print("{} items in dendrogram".format(len_d))

    gids2names.load_groups_file("data/groups.txt")

    for level in range(len_d):
        print()
        partition = community.partition_at_level(dendrogram, level)
        modularity = community.modularity(partition, G)
        print("partition at level {} is\n{}".format(level, pformat(partition)))
        print("modularity at level {} is {}".format(level, modularity))
        for com in set(partition.values()):
            list_nodes = sorted([nodes for nodes in partition.keys()
                            if partition[nodes] == com])
            print("nodes: {}".format(json.dumps(list_nodes)))
            print("    groups:")
            for gid, name in gids2names.generate_group_names(
                    group_ids_list=list_nodes):
                print("    {} {}".format(gid, name))

##drawing
#size = float(len(set(partition.values())))
#pos = nx.spring_layout(G)
#count = 0
#for com in set(partition.values()) :
#    count = count + 1
#    list_nodes = [nodes for nodes in partition.keys()
#                                if partition[nodes] == com]
#    print("[{}]: {}".format(count, list_nodes))
#    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
#                                node_color = str(count / size))
#
#nx.draw_networkx_edges(G,pos, alpha=0.5)
#plt.show()


@click.command()
@click.option('--edges-file', 'edges_file', type=click.Path(),
        help='File of graph edges.')
@click.option('--resolution', 'resolution', default=dflt_resolution,
        help='Time parameter.')
def go(edges_file, resolution):
    gen_clusters(edges_file, resolution=0.5)

if __name__ == '__main__':
    go()
