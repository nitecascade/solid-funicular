#!/usr/bin/env python3

import click
import json
import sys

group_names_file = None
group_names = None


def load_groups_file(group_names_file):
    global group_names
    with open(group_names_file) as gfp:
        group_names = dict()
        for line in gfp:
            line = line.strip()
            gid, name = line.split(maxsplit=1)
            group_names[gid] = name
    print("read {} groups".format(len(group_names)))


def generate_group_names(group_ids_file=None, group_ids_list=None,
        group_ids_json=None, group_ids_str=None):
    gid_set = set()
    if group_ids_file:
        with click.open_file(group_ids_file) as gfp:
            for line in gfp:
                for gid in line.split():
                    gid_set.add(gid)
    if group_ids_json:
        for gid in json.loads(group_ids_list):
            gid_set.add(str(gid))
    if group_ids_list:
        for gid in group_ids_list:
            gid_set.add(gid)
    if group_ids_str:
        for gid in group_ids_str.split():
            gid_set.add(gid)
    for gid in sorted(gid_set):
        yield gid, group_names[gid]


@click.command()
@click.option('--gids-file', 'group_ids_file', type=click.Path(),
        help='File of group_ids.')
@click.option('--gids-json', 'group_ids_json', help='group_ids, JSON string.')
@click.option('--gids', 'group_ids_str', help='group_ids, space separated.')
def go(group_ids_file, group_ids_json, group_ids_str):
    print("group_ids_file: {!r}".format(group_ids_file))
    print("group_ids_json: {!r}".format(group_ids_json))
    print("group_ids_str: {!r}".format(group_ids_str))
    all_names = generate_group_names(
                    group_ids_file=group_ids_file,
                    group_ids_str=group_ids_str,
                    group_ids_json=group_ids_json,
                    )
    for gid, name in all_names:
        print("{} {}".format(gid, name))

if __name__ == '__main__':
    load_groups_file("data/groups.txt")
    go()
