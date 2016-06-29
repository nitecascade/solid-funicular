#!/usr/bin/env python

import igraph as ig

g = ig.Graph.Read_Ncol("data/200_edges_no_dups.ncol", directed=False)
ig.summary(g)

layout = g.layout("kk")

style = dict()
style["vertex_size"] = 10
style["edge_width"] = [1 + w/1000 for w in g.es["weight"]]
style["layout"] = layout
ig.plot(g, **style)
