#!/usr/bin/env python3

from functools import partial
import click
import random
from meetupdata import gen_group_id_and_member_ids

dflt_seed = None
dflt_k = 1
dflt_num = 100


def gen_random_edges_common_members(stash_root, k=dflt_k, n=dflt_num,
        seed=dflt_seed):
    """
    Generate at most n random edges of the group graph from the JSON data
    stored in a directory stash. An edge between groups g1 and g2 means there
    are at least k members who belongs to both.
    """

    if n == -1:
        n = dflt_num

    random.seed(seed)
    sample = random.sample

    # Build a dict containing all the group_ids as keys, with the corresponding
    # member_id set as the value.

    node_data = dict()
    gen = gen_group_id_and_member_ids(stash_root)
    for group_id, member_ids in gen:
        node_data[group_id] = member_ids
    print("{} groups".format(len(node_data)))

    # The nodes of the graph are the group_ids. Two nodes are connected with an
    # edge if they have at least k member_ids in common. Generate at most n
    # random unique undirected edges where the intersection of their member_id
    # sets has at least k members. The output consists of the node pairs
    # (node1, node2) and the edge weight (the number of member_ids those two
    # nodes have in common.

    edges = set()
    num_emitted = 0
    node_list = sorted(node_data)
    while num_emitted < n:
        n1, n2 = sample(node_list, 2)
        n1, n2 = min(n1, n2), max(n1, n2)
        if (n1, n2) not in edges:
            edges.add((n1, n2))
            common_member_ids = node_data[n1].intersection(node_data[n2])
            num_common = len(common_member_ids)
            if num_common >= k:
                yield str(n1), str(n2), num_common
                num_emitted += 1
                if num_emitted % 100 == 0:
                    print(".", end="", flush=True)
                if num_emitted % 1000 == 0:
                    print("{}".format(num_emitted), end="", flush=True)
    print()
    print("{} edges".format(num_emitted))


def gen_edges_common_members(stash_root, k=dflt_k, n=dflt_num):
    """
    Generate at most n edges of the group graph from JSON data stored in a
    directory stash. An edge between groups g1 and g2 means there are at least
    k members who belongs to both.
    """

    if n == -1:
        n = dflt_num

    # Build a dict containing all the group_ids as keys, with the corresponding
    # member_id set as the value.

    node_data = dict()
    gen = gen_group_id_and_member_ids(stash_root)
    for group_id, member_ids in gen:
        node_data[group_id] = member_ids
    print("{} groups".format(len(node_data)))

    # The nodes of the graph are the group_ids. Two nodes are connected with an
    # edge if they have at least k member_ids in common. Generate all unique
    # undirected edges where the intersection of their member_id sets has at
    # least k members. The output consists of the node pairs (node1, node2)
    # and the edge weight (the number of member_ids those two nodes have
    # in common.

    num_emitted = 0
    for n1 in node_data:
        for n2 in node_data:
            if n1 > n2:     # Do not emit b--a if a--b was already emitted.
                continue
            if n1 == n2:    # Do not emit self loops.
                continue
            common_member_ids = node_data[n1].intersection(node_data[n2])
            num_common = len(common_member_ids)
            if num_common >= k:
                yield str(n1), str(n2), num_common
                num_emitted += 1
                if num_emitted % 100 == 0:
                    print(".", end="", flush=True)
                if num_emitted % 1000 == 0:
                    print("{}".format(num_emitted), end="", flush=True)
                if num_emitted >= n:
                    break
        else:
            continue
        break
    print("{} edges".format(num_emitted))


@click.command()
@click.option("-k", default=dflt_k,
        help="""Two groups must have at least k members in common to have
            an edge between them.""")
@click.option("-n", default=dflt_num,
        help="""Produce at most num edges; use -1 to produce all edges
            (for --random-sample, -1 just selects the default.""")
@click.option("--random-sample", is_flag=True,
        help="""Generate edges randomly. Without this option
                generates all edges.""")
@click.option("--seed", default=dflt_seed,
        help="""Seed for random number generator.""")
@click.argument('stash-root', type=click.Path())
@click.argument('ncol-file', type=click.Path())
def go(k, n, random_sample, seed, stash_root, ncol_file):
    """
    Walk the directory tree starting at stash-root, read each group-member
    JSON file found, generate the group graph, and finally write the weighted
    edges of to ncol-file.

    The NCOL output format is:

        \b
        node1 node2 weight
        node3 node4 weight
        ...
    """
    print("stash_root: {!r}".format(stash_root))
    print("random_dample: {}".format(random_sample))
    print("k: {}".format(k))
    print("n: {}".format(n))
    print("seed: {}".format(seed))
    if random_sample:
        gen = partial(gen_random_edges_common_members, seed=seed)
    else:
        gen = partial(gen_edges_common_members)
    with click.open_file(ncol_file, "w") as ofp:
        for n1, n2, w in gen(stash_root, k=k, n=n):
            print("{} {} {}".format(n1, n2, w), file=ofp)

if __name__ == '__main__':
    go()
