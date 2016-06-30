#!/usr/bin/env python3

from functools import partial
from itertools import combinations
import click
import random
from meetupdata import gen_group_id_and_member_ids

dflt_seed = None
dflt_k = 1
dflt_num = 100


def gen_random_3cliques(stash_root, k=dflt_k, n=dflt_num, seed=dflt_seed):
    """
    Generate at most n the edges of the group graph from JSON data stored in
    a directory stash. Constructs at most n random triangles (3-cliques) where
    the three nodes of a triangle have at least k members in common.
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

    # The nodes of the graph are the group_ids. Construct triangles (three
    # edges) where the number of members in common among the three nodes
    # is at least k. The weight of each edge is the number of members in
    # common for those two nodes.
    #
    # Generate random triangle from the set of nodes.

    edges = set()
    count_tris_found, count_tris_emitted, count_edges_emitted = 0, 0, 0
    node_list = sorted(node_data)
    while count_tris_emitted < n:
        n1, n2, n3 = sample(node_list, 3)
        s = set([n1, n2, n3])
        n1, n3 = min(n1, n2, n3), max(n1, n2, n3)
        n2 = (s - set([n1, n3])).pop()
        count_tris_found += 1
        if n1 > n2:     # Do not emit b--a if a--b was already emitted.
            continue
        if n1 > n3:     # Do not emit b--a if a--b was already emitted.
            continue
        if n2 > n3:     # Do not emit b--a if a--b was already emitted.
            continue
        if n1 == n2:    # Do not emit self loops.
            continue
        if n1 == n3:    # Do not emit self loops.
            continue
        if n2 == n3:    # Do not emit self loops.
            continue
        common_members_12 = node_data[n1].intersection(node_data[n2])
        common_members_13 = node_data[n1].intersection(node_data[n3])
        common_members_23 = node_data[n2].intersection(node_data[n3])
        common_members_123 = common_members_12.intersection(node_data[n3])
        if len(common_members_123) >= k:
            count_tris_emitted += 1
            if (n1, n2) not in edges:   # Do not emit an edge more than once.
                count_edges_emitted += 1
                yield str(n1), str(n2), len(common_members_12)
                edges.add((n1, n2))
            if (n1, n3) not in edges:   # Do not emit an edge more than once.
                count_edges_emitted += 1
                yield str(n1), str(n3), len(common_members_13)
                edges.add((n1, n3))
            if (n2, n3) not in edges:   # Do not emit an edge more than once.
                count_edges_emitted += 1
                yield str(n2), str(n3), len(common_members_23)
                edges.add((n2, n3))
            if count_tris_emitted % 100 == 0:
                print(".", end="", flush=True)
            if count_tris_emitted % 1000 == 0:
                print("{}".format(count_tris_emitted), end="", flush=True)
            if count_tris_emitted >= n:
                break
    print()
    print("{} edges".format(count_tris_emitted))


def gen_3cliques(stash_root, k=dflt_k, n=dflt_num):
    """
    Generate at most n the edges of the group graph from JSON data stored in
    a directory stash. Constructs at most n triangles (3-cliques) where the
    three nodes of a triangle have at least k members in common.
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

    # The nodes of the graph are the group_ids. Construct triangles (three
    # edges) where the number of members in common among the three nodes
    # is at least k. The weight of each edge is the number of members in
    # common for those two nodes.

    edges = set()
    node_list = sorted(node_data)
    count_tris_found, count_tris_emitted, count_edges_emitted = 0, 0, 0
    for n1, n2, n3 in combinations(node_list, 3):
        print("n1, n2, n3: {} {} {}".format(n1, n2, n3))
        count_tris_found += 1
        if n1 > n2:     # Do not emit b--a if a--b was already emitted.
            continue
        if n1 > n3:     # Do not emit b--a if a--b was already emitted.
            continue
        if n2 > n3:     # Do not emit b--a if a--b was already emitted.
            continue
        if n1 == n2:    # Do not emit self loops.
            continue
        if n1 == n3:    # Do not emit self loops.
            continue
        if n2 == n3:    # Do not emit self loops.
            continue
        common_members_12 = node_data[n1].intersection(node_data[n2])
        common_members_13 = node_data[n1].intersection(node_data[n3])
        common_members_23 = node_data[n2].intersection(node_data[n3])
        common_members_123 = common_members_12.intersection(node_data[n3])
        print("common members: {}".format(common_members_123))
        if len(common_members_123) >= k:
            count_tris_emitted += 1
            if (n1, n2) not in edges:   # Do not emit an edge more than once.
                count_edges_emitted += 1
                yield str(n1), str(n2), len(common_members_12)
                edges.add((n1, n2))
            if (n1, n3) not in edges:   # Do not emit an edge more than once.
                count_edges_emitted += 1
                yield str(n1), str(n3), len(common_members_13)
                edges.add((n1, n3))
            if (n2, n3) not in edges:   # Do not emit an edge more than once.
                count_edges_emitted += 1
                yield str(n2), str(n3), len(common_members_23)
                edges.add((n2, n3))
            if count_tris_emitted % 100 == 0:
                print(".", end="", flush=True)
            if count_tris_emitted % 1000 == 0:
                print("{}".format(count_tris_emitted), end="", flush=True)
            if count_tris_emitted >= n:
                break
            
    print()
    print("{} triangles found".format(count_tris_found))
    print("{} triangles emitted".format(count_tris_emitted))
    print("{} edges emitted".format(count_edges_emitted))

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
    print("random_sample: {}".format(random_sample))
    print("k: {}".format(k))
    print("n: {}".format(n))
    print("seed: {}".format(seed))
    if random_sample:
        gen = partial(gen_random_3cliques, seed=seed)
    else:
        gen = partial(gen_3cliques)
    with click.open_file(ncol_file, "w") as ofp:
        for n1, n2, w in gen(stash_root, k=k, n=n):
            print("{} {} {}".format(n1, n2, w), file=ofp)

if __name__ == '__main__':
    go()