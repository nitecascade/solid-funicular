#!/usr/bin/env python3

import re
import sys

class GroupGraphGen:
    def __init__(self, gen):
        """
        The Meetup Group Graph is an undirected graph where the nodes represent
        Meetup groups (group_id) and an edge of weight W between two nodes
        indicates the two groups have W members in common.
        
        The graph file in NCOL format consists of lines with fields::

            group_id1 group_id2 weight

        The edges are undirected. The graph file should not contain the edge (B
        A W) if it contains the edge (A B W). Such redundant edges can be
        removed by the method::

            .filter_dups()   

        which removes the one that comes lexicographically second. Note that
        filter_dups() has to save the edges (so it can tell when it has seen an
        edge before) so it is memory intensive.

        This class creates an instance from a generator of edges. When the
        source of the edges is a file, the classmethod::

            from_file(graph_file)

        creates an initial generator.
        
        The edges generated by the instance can be filtered using the methods::

            .filter_edges_by_weight_range(...)
            .filter_edges_by_gid_regexes(...)
        """
        self.gen = gen

    @classmethod
    def from_file(cls, graph_file):
        def reader():
            with open(graph_file) as gfp:
                for line in gfp:
                    line = line.strip()
                    #print("line = {}".format(line))
                    gid1, gid2, weight = line.split()
                    yield str(gid1), str(gid2), int(weight)
        return cls(reader())

    def __iter__(self):
        """
        A generator that produces each edge of the graph as a tuple
        (str(gid_1), str(gid_2), int(weight)).
        """
        yield from self.gen

    def filter(self, gen):
        return self.__class__(gen)

    def filter_edges_by_weight_range(self, min_weight=None, max_weight=None):
        """
        A generator that filters the nodes of the graph by weight range.
        """
        def weight_filter():
            for g1, g2, w in self.gen:
                ok_min = ok_max = True
                if min_weight is not None and w < min_weight:
                    ok_min = False
                #else:
                #    print("min ok: {} >= {}".format(w, min_weight))
                if max_weight is not None and w > max_weight:
                    ok_max = False
                #else:
                #    print("max ok: {} <= {}".format(w, max_weight))
                if ok_min and ok_max:
                    yield g1, g2, w
        return self.filter(weight_filter())

    def filter_edges_by_gid_regexes(self, regex_list=None):
        """
        A generator that filters the nodes of the graph by group_ids
        matching any of a list of regexes.
        """
        def regex_filter():
            for g1, g2, w in self.gen:
                matched = False
                for r in regex_list:
                    if r.match(g1) and r.match(g2):
                        matched = True
                        break
                if matched:
                    yield g1, g2, w
        return self.filter(regex_filter())

    def filter_dups(self):
        """
        A generator that filters out duplicate edges.
        """
        def dups_filter():
            dups = set()
            for g1, g2, w in self.gen:
                if (min(g1, g2), max(g1, g2)) in dups:
                    continue
                dups.add((min(g1, g2), max(g1, g2)))
                yield g1, g2, w
        return self.filter(dups_filter())
