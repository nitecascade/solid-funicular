#!/usr/bin/env python3

from functools import partial
from itertools import combinations
import click
import os
import random
from meetupdata import GroupsData

dflt_seed = None
dflt_k = 1      # Number of members two groups must have in common.
dflt_p = 0.05   # Percent membership each of two groups must share.
dflt_num = 100  # Number of edges to generate.
dflt_max_null_passes=10000  # Stop if no random edge after this many trys.


def gen_random_3cliques(source, k=None, p=None, n=None, seed=None,
        max_null_passes=None):
    """
    Generate at most n the edges of the group graph from JSON data stored in a
    directory stash or a file (source extension is ".json"). Constructs at most
    n random triangles (3-cliques) where the three nodes of a triangle have at
    least k members in common.
    """

    if not k and not p:
        raise RuntimeError("specify k or p, or both!")
    if k is None:
        k = dflt_k
    if p is None:
        p = dflt_p
    if max_null_passes is None:
        max_null_passes = dflt_max_null_passes
    if n is None or n < 0:
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
        #node_data[gid] = [_[0] for _ in gdata["members"]]
        node_data[gid] = gdata["members"]
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
    null_passes = 0
    while count_tris_emitted < n:
        if null_passes >= max_null_passes:
            print("quitting: no new edges for {} random samples".format(
                max_null_passes))
            break
        emmited_one = False
        n1, n2, n3 = sample(node_list, 3)
        s = set([n1, n2, n3])
        n1, n3 = min(n1, n2, n3), max(n1, n2, n3)
        n2 = (s - set([n1, n3])).pop()
        count_tris_found += 1
        if n1 > n2:     # Do not emit b--a if a--b was already emitted.
            null_passes += 1
            continue
        if n1 > n3:     # Do not emit b--a if a--b was already emitted.
            null_passes += 1
            continue
        if n2 > n3:     # Do not emit b--a if a--b was already emitted.
            null_passes += 1
            continue
        if n1 == n2:    # Do not emit self loops.
            null_passes += 1
            continue
        if n1 == n3:    # Do not emit self loops.
            null_passes += 1
            continue
        if n2 == n3:    # Do not emit self loops.
            null_passes += 1
            continue
        set_n1 = set(node_data[n1])
        set_n2 = set(node_data[n2])
        set_n3 = set(node_data[n3])
        common_members_12 = set_n1.intersection(set_n2)
        common_members_13 = set_n1.intersection(set_n3)
        common_members_23 = set_n2.intersection(set_n3)
        common_members_123 = common_members_12.intersection(set_n3)
        k_good_to_go = True
        p_good_to_go = True
        if k:
            num_common_123 = len(common_members_123)
            if num_common_123 < k:
                k_good_to_go = False
        if p:
            num_common_123 = len(common_members_123)
            num_common_12 = len(common_members_12)
            num_common_13 = len(common_members_13)
            num_common_23 = len(common_members_23)
            if (
                    min(num_common_12, num_common_13, num_common_23) == 0
                    or max(num_common_123/num_common_12,
                            num_common_123/num_common_13,
                            num_common_123/num_common_23) < p)
                ):
                p_good_to_go = False
        if k_good_to_go or p_good_to_go:
            count_tris_emitted += 1
            if (n1, n2) not in edges:   # Do not emit an edge more than once.
                count_edges_emitted += 1
                emmited_one = True
                yield str(n1), str(n2), len(common_members_12)
                edges.add((n1, n2))
            if (n1, n3) not in edges:   # Do not emit an edge more than once.
                count_edges_emitted += 1
                emmited_one = True
                yield str(n1), str(n3), len(common_members_13)
                edges.add((n1, n3))
            if (n2, n3) not in edges:   # Do not emit an edge more than once.
                count_edges_emitted += 1
                emmited_one = True
                yield str(n2), str(n3), len(common_members_23)
                edges.add((n2, n3))
            if count_tris_emitted % 100 == 0:
                print(".", end="", flush=True)
            if count_tris_emitted % 1000 == 0:
                print("{}".format(count_tris_emitted), end="", flush=True)
            if count_tris_emitted >= n:
                break
        if not emmited_one:
            null_passes += 1
    print()
    print("{} edges".format(count_tris_emitted))


def gen_3cliques(source, k=None, p=None, n=None):
    """
    Generate at most n edges of the group graph from JSON data stored in a
    directory stash or file (source extension .json). Constructs at most n
    triangles (3-cliques) where the three nodes of a triangle have at least k
    members in common.
    """

    if not k and not p:
        raise RuntimeError("specify k or p, or both!")
    if k is None:
        k = dflt_k
    if p is None:
        p = dflt_p
    if n is None:
        n = dflt_num

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
        #node_data[gid] = [_[0] for _ in gdata["members"]]
        node_data[gid] = gdata["members"]
    print("{} groups".format(len(node_data)))

    # The nodes of the graph are the group_ids. Construct triangles (three
    # edges) where the number of members in common among the three nodes
    # is at least k. The weight of each edge is the number of members in
    # common for those two nodes.

    edges = set()
    node_list = sorted(node_data)
    count_tris_found, count_tris_emitted, count_edges_emitted = 0, 0, 0
    for n1, n2, n3 in combinations(node_list, 3):
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
        set_n1 = set(node_data[n1])
        set_n2 = set(node_data[n2])
        set_n3 = set(node_data[n3])
        common_members_12 = set_n1.intersection(set_n2)
        common_members_13 = set_n1.intersection(set_n3)
        common_members_23 = set_n2.intersection(set_n3)
        common_members_123 = common_members_12.intersection(set_n3)
        k_good_to_go = True
        p_good_to_go = True
        if k:
            num_common_123 = len(common_members_123)
            if num_common_123 < k:
                k_good_to_go = False
        if p:
            num_common_123 = len(common_members_123)
            num_common_12 = len(common_members_12)
            num_common_13 = len(common_members_13)
            num_common_23 = len(common_members_23)
            if (
                    min(num_common_12, num_common_13, num_common_23) == 0
                    or max(num_common_123/num_common_12,
                            num_common_123/num_common_13,
                            num_common_123/num_common_23) < p)
                ):
                p_good_to_go = False
        if k_good_to_go or p_good_to_go:
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
            if n >= 0 and count_tris_emitted >= n:
                break
            
    print()
    print("{} triangles found".format(count_tris_found))
    print("{} triangles emitted".format(count_tris_emitted))
    print("{} edges emitted".format(count_edges_emitted))

@click.command()
@click.option("-k", type=int,
        help=("Two groups must have at least k members in common to have"
            " an edge between them."))
@click.option("-p", type=float,
        help=("Two groups must both have at least p percent members in"
            " common to have an edge between them."))
@click.option("-n", default=dflt_num,
        help=("Produce at most num edges; use -1 to produce all edges"
            " (for --random-sample, -1 just selects the default."))
@click.option("--random-sample", is_flag=True,
        help=("Generate edges randomly. Without this option"
                " generates all edges."))
@click.option("--seed", default=dflt_seed,
        help="Seed for random number generator.")
@click.option("--max-null", default=dflt_max_null_passes,
        help="Stop if no random edge after this many trys.")
@click.argument('source', "source", type=click.Path())
@click.argument('ncol-file', type=click.Path())
def go(k, p, n, random_sample, seed, max_null, source, ncol_file):
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
    print("source: {!r}".format(source))
    print("random-sample: {}".format(random_sample))
    print("k: {}".format(k))
    print("p: {}".format(p))
    print("n: {}".format(n))
    print("max-null: {}".format(max_null))
    print("seed: {}".format(seed))
    if random_sample:
        gen = partial(gen_random_3cliques, seed=seed, max_null_passes=max_null)
    else:
        gen = partial(gen_3cliques)
    with click.open_file(ncol_file, "w") as ofp:
        for n1, n2, w in gen(source, k=k, p=p, n=n):
            print("{} {} {}".format(n1, n2, w), file=ofp)

if __name__ == '__main__':
    go()
