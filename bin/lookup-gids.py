#!/usr/bin/env python3

import click
import json
import sys
from meetupdata import GroupGidMapper


if __name__ == '__main__':

    def gather_group_ids(group_ids_file=None, group_ids_list=None,
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
        return gid_set


    def group_values_gen(group_ids_file=None, group_ids_list=None,
            group_ids_json=None, group_ids_str=None, gid_map=None, key=None):
        if key is None:
            key = "name"
        gid_set = gather_group_ids(
                        group_ids_file=group_ids_file,
                        group_ids_list=group_ids_list,
                        group_ids_json=group_ids_json,
                        group_ids_str=group_ids_str,
                        )
        for gid in sorted(gid_set):
            yield gid, gid_map.get(gid, key)

    @click.command()
    @click.option('--gids-file', 'group_ids_file', type=click.Path(),
            help='File of group_ids.')
    @click.option('--gids-json', 'group_ids_json',
            help='group_ids, JSON string.')
    @click.option('--gids', 'group_ids_str',
            help='group_ids, space separated.')
    @click.option('--key', 'key', default="name",
            help='Field to return (name, members, description).')
    @click.option('--groups-file', 'groups_file', type=click.Path(),
            default="data/groups.txt",
            help='File of group information (.json or .txt.')
    def go(group_ids_file, group_ids_json, group_ids_str, key, groups_file):
        print("group_ids_file: {!r}".format(group_ids_file))
        print("group_ids_json: {!r}".format(group_ids_json))
        print("group_ids_str: {!r}".format(group_ids_str))
        print("groups_file: {!r}".format(groups_file))
        gid_map = GroupGidMapper(groups_file)
        gid_map.load()
        print("read {} group names from {!r}".format(
            len(gid_map), gid_map._file))
        all_values = group_values_gen(
                        group_ids_file=group_ids_file,
                        group_ids_str=group_ids_str,
                        group_ids_json=group_ids_json,
                        gid_map=gid_map,
                        key=key,
                        )
        for gid, value in all_values:
            print("{} {}".format(gid, value))

    go()
