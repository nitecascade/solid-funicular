#!/usr/bin/env python3

import click
from groupgraph import GroupGraphGen

def dedup_from_ncol_file(ncol_file):
    yield from GroupGraphGen.from_file(ncol_file).filter_dups() 

@click.command()
@click.argument("ncol_file", type=click.Path())
@click.argument("out_file", type=click.Path())
def go(ncol_file, out_file):
    """
    Removes duplicate edges from an edge-list file. The NCOL format is:

        \b
        node1 node2 weight
        node3 node4 weight
        ...
    """
    with click.open_file(out_file, "w") as ofp:
        for g1, g2, w in dedup_from_ncol_file(ncol_file):
            print("{} {} {}".format(str(g1), str(g2), int(w)), file=ofp)

if __name__ == '__main__':
    go()
