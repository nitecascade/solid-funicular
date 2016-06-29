#!/usr/bin/env python3

import re
import sys
from groupgraph import GroupGraphGen

#r = [re.compile(r"^2.*")]
r = [re.compile(r".")]
#group_graph = GroupGraphGen.from_file("data/2000_edges.txt")
#group_graph = GroupGraphGen.from_file("data/200_edges.txt")
#group_graph = GroupGraphGen.from_file("10_edges_sorted.txt")
group_graph = GroupGraphGen.from_file("data/50_edges.ncol")
#group_graph = GroupGraphGen.from_file(
#        "really_big_data/really_big_data_sorted.out")

#for g1, g2, w in group_graph:
#    print("{} {}: {}".format(g1, g2, w))
#sys.exit()

edges = (group_graph
            .filter_dups()
            #.filter_edges_by_weight_range(min_weight=10)
            #.filter_edges_by_gid_regexes(r)
            )

with open("50_edges_no_dups.ncol", "w") as out_fp:
    count = 0
    for g1, g2, w in edges:
        count += 1
        print("{} {} {}".format(g1, g2, w), file=out_fp)
    print("{} edges".format(count))
