#!/usr/bin/env python3

from functools import partial
import click
from pprint import pformat
import os
import random
from meetupdata import GroupsData

dflt_seed = None
dflt_k = 1
dflt_num = 100


def gen_random_edges_common_members(source, k=dflt_k, n=dflt_num,
        seed=dflt_seed):
    """
    Generate at most n random edges of the group graph from the JSON data
    stored in a directory stash or file (source extension ".json"). An edge
    between groups g1 and g2 means there are at least k members who belongs to
    both.
    """

    if n == -1:
        n = dflt_num

    random.seed(seed)
    sample = random.sample

    # Build a dict containing all the group_ids as keys, with the corresponding
    # member_id set as the value.

    ext = os.path.splitext(source)[1]
    if ext == ".json":
        g = GroupsData.from_file(source)
    else:
        g = GroupsData.from_stash(source)

    node_data = dict()
    for gid in g.get_gids():
        gdata = g.lookup_gid(gid)
        node_data[gid] = [_[0] for _ in gdata["members"]]
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
    null_passes, max_null_passes = 0, 1000
    while num_emitted < n:
        if null_passes >= max_null_passes:
            print("quitting: no new edges for {} random samples".format(
                max_null_passes))
            break
        n1, n2 = sample(node_list, 2)
        n1, n2 = min(n1, n2), max(n1, n2)
        if (n1, n2) not in edges:
            edges.add((n1, n2))
            common_member_ids = set(node_data[n1]).intersection(
                    set(node_data[n2]))
            num_common = len(common_member_ids)
            if num_common >= k:
                yield str(n1), str(n2), num_common
                num_emitted += 1
                null_passes = 0
                if num_emitted % 100 == 0:
                    print(".", end="", flush=True)
                if num_emitted % 1000 == 0:
                    print("{}".format(num_emitted), end="", flush=True)
        else:
            null_passes += 1
    print()
    print("{} edges".format(num_emitted))


def gen_edges_common_members(source, k=dflt_k, n=dflt_num):
    """
    Generate at most n edges of the group graph from JSON data stored in a
    directory stash or a file (source extension .json). An edge between groups
    g1 and g2 means there are at least k members who belongs to both.
    """

    if n == -1:
        n = dflt_num

    # Build a dict containing all the group_ids as keys, with the corresponding
    # member_id set as the value.

    ext = os.path.splitext(source)[1]
    if ext == ".json":
        g = GroupsData.from_file(source, fields=["id"])
    else:
        g = GroupsData.from_stash(source, fields=["id"])

    node_data = dict()
    for gid in g.get_gids():
        gdata = g.lookup_gid(gid)
        node_data[gid] = [_[0] for _ in gdata["members"]]
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
            common_member_ids = set(node_data[n1]).intersection(
                    set(node_data[n2]))
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
        help=("Two groups must have at least k members in common to have"
            " an edge between them."))
@click.option("-n", default=dflt_num,
        help=("Produce at most num edges; use -1 to produce all edges"
            " (for --random-sample, -1 just selects the default."))
@click.option("--random-sample", is_flag=True,
        help=("Generate edges randomly. Without this option"
                " generates all edges."))
@click.option("--seed", default=dflt_seed,
        help="Seed for random number generator.")
@click.argument('source', type=click.Path())
@click.argument('ncol-file', type=click.Path())
def go(k, n, random_sample, seed, source, ncol_file):
    """
    Generate the group graph from the source (either a directory stash or a
    file of JSON group objects), and finally write the weighted edges of to
    ncol-file.

    The NCOL output format is:

        \b
        node1 node2 weight
        node3 node4 weight
        ...
    """
    print("source: {!r}".format(source))
    print("random_dample: {}".format(random_sample))
    print("k: {}".format(k))
    print("n: {}".format(n))
    print("seed: {}".format(seed))
    if random_sample:
        gen = partial(gen_random_edges_common_members, seed=seed)
    else:
        gen = partial(gen_edges_common_members)
    with click.open_file(ncol_file, "w") as ofp:
        for n1, n2, w in gen(source, k=k, n=n):
            print("{} {} {}".format(n1, n2, w), file=ofp)

if __name__ == '__main__':
    go()
