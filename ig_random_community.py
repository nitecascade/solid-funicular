#!/usr/bin/env python

import louvain
import igraph as ig

G = ig.Graph.Erdos_Renyi(100, 0.1)
G.es['weight'] = 1.0
part = louvain.find_partition(G, method='Modularity', weight='weight')
print(part.quality)
part.significance = louvain.quality(G, part, method='Significance')
print(part.significance)

layout = G.layout("kk")

style = dict()
style["vertex_size"] = 10
style["edge_width"] = [1 + w/1000 for w in G.es["weight"]]
style["layout"] = layout
ig.plot(G, **style)

import pandas as pd
import matplotlib.pyplot as plt
res_parts = louvain.bisect(G, method='CPM', resolution_range=[0,1])
keys = list(res_parts.keys())
print("res_parts.keys(): {}".format(keys))
print("res_parts.values(): {}".format(res_parts.values()))

res_df = pd.DataFrame({
         'resolution': keys,
         'bisect_value': [bisect.bisect_value for bisect in res_parts.values()],
         })
plt.step(res_df['resolution'], res_df['bisect_value'])
plt.xscale('log')
plt.show()
