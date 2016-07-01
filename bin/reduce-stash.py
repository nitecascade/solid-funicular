#!/usr/bin/env python

import click
import sys
from meetupdata import GroupsData

if __name__ == '__main__':

    @click.command()
    @click.option("--check/--no-check",
            help=("After writing the output file, check that it has"
                    " the same group_ids as the stash."))
    @click.argument("stash-root", type=click.Path())
    @click.argument("groups-file", type=click.Path())
    def go(check, stash_root, groups_file):
        """
        Read the stash located at stash-root and write the groups data to
        a file at groups-file. Only the fields "group_id" and the corresponding
        list of member ids will be written.
        """
        print("stash-root: {}".format(stash_root))
        print("groups-file: {}".format(groups_file))
        print("check: {}".format(check))
        with click.open_file(groups_file, "w") as ofp:
            g = GroupsData.from_stash(stash_root, fields=["id"])
            g.write_member_ids(groups_file)
        if check:
            g_gids = g.get_gids()
            g2 = GroupsData.from_file(groups_file)
            g2_gids = g2.get_gids()
            len_gids = len(g_gids)
            len_gids2 = len(g2_gids)
            if len_gids == len_gids2 and sorted(g_gids) == sorted(g2_gids):
                print("ok: checked {} gids in stash and groups file".format(
                    len(g_gids)))
            else:
                len_gids = len(g_gids)
                len_gids2 = len(g2_gids)
                print("mismatch: stash and groups file have different gids!")
                sys.exit(1)
    go()
