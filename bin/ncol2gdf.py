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
    edges = set()
    num_edges, num_dups = 0, 0
    for line in ncol_fp:
        num_edges += 1
        line = line.strip()
        n1, n2, w = line.split()
        n1, n2 = min(n1, n2), max(n1, n2)
        if (n1, n2) in edges:
            # This edge has already been seen.
            num_dups += 1
            continue
        edges.add((n1, n2))
        w = int(w)
        yield n1, n2, w
    print("read {} edges ({} dups)".format(num_edges, num_dups))


@click.command()
@click.argument('ncol-file', type=click.Path())
@click.argument('gdf-file', type=click.Path())
def go(ncol_file, gdf_file):
    """
    Convert a group graph file from NCOL format to GDF format.
    """
    with click.open_file(ncol_file) as ncol_fp:
        nodes = get_nodes(ncol_fp)
    print("read {} nodes".format(len(nodes)))
    with click.open_file(ncol_file) as ncol_fp:
        with click.open_file(gdf_file, "w") as gdf_fp:
            print("nodedef>name VARCHAR", file=gdf_fp)
            num_nodes = 0
            for n in sorted(nodes):
                num_nodes += 1
                print("{}".format(n), file=gdf_fp)
            print("wrote {} nodes".format(num_nodes))
            print("edgedef>node1 VARCHAR,node2 VARCHAR,weight INT", file=gdf_fp)
            num_edges = 0
            for n1, n2, w in edges_gen(ncol_fp):
                num_edges += 1
                print("{},{},{}".format(n1, n2, w), file=gdf_fp)
            print("wrote {} edges".format(num_edges))

if __name__ == '__main__':
    go()
