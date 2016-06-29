#!/usr/bin/env python

import click


def get_nodes(ncol_fp):
    nodes = set()
    for line in ncol_fp:
        line = line.strip()
        n1, n2, _ = line.split()
        nodes.add(n1)
        nodes.add(n2)
    return nodes


def edges_gen(ncol_fp):
    nodes = set()
    for line in ncol_fp:
        line = line.strip()
        n1, n2, w = line.split()
        if n2 in nodes: # This means n2 has already appeared as n1.
            continue
        nodes.add(n1)
        w = int(w)
        yield n1, n2, w


@click.command()
@click.argument('ncol-file', type=click.Path())
@click.argument('gdf-file', type=click.Path())
def go(ncol_file, gdf_file):
    """
    Convert a group graph file from NCOL format to GDF format.
    """
    with click.open_file(ncol_file) as ncol_fp:
        nodes = get_nodes(ncol_fp)
    with click.open_file(ncol_file) as ncol_fp:
        with click.open_file(gdf_file, "w") as gdf_fp:
            print("nodedef>name VARCHAR", file=gdf_fp)
            for n in sorted(nodes):
                print("{}".format(n), file=gdf_fp)
            print("edgedef>node1 VARCHAR,node2 VARCHAR,weight INT", file=gdf_fp)
            for n1, n2, w in edges_gen(ncol_fp):
                print("{},{},{}".format(n1, n2, w), file=gdf_fp)

if __name__ == '__main__':
    go()
