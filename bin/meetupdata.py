#!/usr/bin/env python3

import json
import os
import sys


class GroupGidMap:
    """
    Class to create a map from gid to basic group info.
    """

    def __init__(self, map):
        """
        The class constructor is not typically invoked directly. Use one
        of the from_xxx classmethods below.
        """
        self._group_gid_map = map

    @classmethod
    def from_file(cls, groups_file):
        """
        A groups file can be either a plain text file (xxx.txt) or a file
        of JSON objects (xxx.json). This classmethod determines which to
        use based on file extension and uses the appropriate loader.
        """
        ext = os.path.splitext(groups_file)[1]
        if ext == ".txt":
            return cls(map=cls._load_txt(groups_file))
        if ext == ".json":
            return cls(map=cls._load_json(groups_file))

    @staticmethod
    def _load_txt(fpath):
        """
        Loads basic info for groups from a plain file. The file format is:

            gid1 This group's name
            gid2 Some other group's name
            ...
        """
        group_gid_map = dict()
        with open(fpath) as gfp:
            for line in gfp:
                line = line.strip()
                gid, name = line.split(maxsplit=1)
                group_gid_map[gid] = dict(name=name)
        return group_gid_map

    @staticmethod
    def _load_json(fpath):
        """
        Loads basic info for groups from a JSON file. The file format is:

            {"key1": value1, ...}
            {"key2": value2, ...}

        There should be keys for "id", "members", and optionally "description".
        """
        group_gid_map = dict()
        with open(fpath) as gfp:
            for line in gfp:
                line = line.strip()
                jobj = json.loads(line)
                gid = str(jobj["id"])
                name = jobj["name"]
                members = jobj["members"]
                description = jobj.get("description", "<none>")
                group_gid_map[gid] = dict(
                        name=name,
                        members=members,
                        description=description,
                        )
        return group_gid_map

    def get(self, gid, key):
        """
        Return the value of key for gid.
        """
        if self._group_gid_map is None:
            self.load()
        return self._group_gid_map[gid][key]

    def __getitem__(self, gid):
        """
        By default, return the "name" field when accessed with x[gid]. To
        access some other field, use the get() method.
        """
        if self._group_gid_map is None:
            self.load()
        return self._group_gid_map[gid]["name"]

    def __setitem__(self, key, value):
        raise RuntimeError("group_gid to group_name map is immutable!")

    def __len__(self):
        return len(self._group_gid_map)

    def __iter__(self):
        return iter(self._group_gid_map)

    def __contains__(self, item):
        return item in self.group_id_map


def gen_group_id_and_file_path(stash_root):
    """
    The stash directory contains:
        stash/
            members_in_group_/
                1/2/12345.json
                1/2/12678.json
                ...
    This generator yields:
        12345, members_in_group_/1/2/12345.json
        12678, members_in_group_/1/2/12678.json
    where 12345 is a group_id
        ...
    """
    for dir_name, subdir_list, file_list in os.walk(stash_root):
        for fname in file_list:
            group_id = os.path.splitext(fname)[0]
            yield group_id, os.path.join(dir_name, fname)


class GroupsStashData:
    """
    Class for accessing group data located in a directory stash.
    """

    def __init__(self, stash_root, fields=None):
        self._stash_root = stash_root
        self._fields = fields
        self._gid_list = None

    def lookup_gid(self, gid, fields=None):
        """
        Return the group data for this gid.
        """
        if fields is None:
            fields = self._fields
        if fields is None:
            fields = ["id"]
        level_1, level_2 = str(gid)[:2]
        fname = str(gid) + ".json"
        fpath = os.path.join(self._stash_root, level_1, level_2, fname)
        group_dict = dict(gid=gid)
        member_list = []
        with open(fpath) as gfp:
            for line in gfp:
                line = line.strip()
                envelope = json.loads(line)
                envelope_gid = envelope["group_id"]
                envelope_member = envelope["member"]
                member = dict()
                for f in fields:
                    member[f] = envelope_member[f]
                member_list.append(tuple(member.values()))
        group_dict["members"] = member_list
        return group_dict

    def get_gids(self):
        """
        Return the list of gids.
        """
        if not self._gid_list:
            gid_list = []
            for dir_name, subdir_list, file_list in os.walk(self._stash_root):
                for fname in file_list:
                    gid = os.path.splitext(fname)[0]
                    gid_list.append(gid)
            self._gid_list = gid_list
        return self._gid_list


class GroupsFileData:
    """
    Class for accessing group data located in a file.
    """

    def __init__(self, fpath, fields=None):
        self._fpath = fpath
        self._fields = fields
        self._groups_dict = self._load(self._fpath)
        self._gid_list = None

    @staticmethod
    def _load(fpath):
        groups_dict = dict()
        with open(fpath) as gfp:
            for line in gfp:
                line = line.strip()
                envelope = json.loads(line)
                envelope_gid = envelope["gid"]
                envelope_member = envelope["member"]
                if self._fields:
                    member = dict()
                    for f in self._fields:
                        member[f] = envelope_member[f]
                else:
                    member = envelope_member
                groups_dict[envelope_gid] = member
        return groups_dict

    def lookup_gid(self, gid, fields=None):
        """
        Return the group data for this gid.
        """
        if fields is None:
            fields = self._fields
        if fields is None:
            return self._groups_dict[gid]
        gid_data = self._groups_dict[gid]
        if fields is None:
            caller_gid_data = gid_data
        else:
            caller_gid_data = dict()
            for f in fields:
                caller_gid_data[f] = gid_data[f]
        return caller_gid_data

    def get_gids(self):
        """
        Return the list of gids.
        """
        if not self._gid_list:
            self._gid_list = self._groups_dict.keys()
        return self._gid_list


class GroupsData:

    """
    Access Meetup group data from the raw datafiles downloaded from Meetup.com
    (called a stash) or from a single file that rolls up that data. This class
    provides methods to read group data by gid.
    """

    def __init__(self, groups_data, fields=None):
        self._groups_data = groups_data
        self._fields = fields

    @classmethod
    def from_stash(cls, stash_root, fields=None):
        """
        Access Meetup group data from a directory stash of JSON files.
        """
        if fields is None:
            fields = ["id"]
        stash_data = GroupsStashData(stash_root=stash_root, fields=fields)
        return cls(groups_data=stash_data, fields=fields)

    @classmethod
    def from_file(cls, fpath, fields=None):
        """
        Access Meetup group data from a JSON file.
        """
        file_data = GroupsFileData(fpath=fpath, fields=fields)
        return cls(groups_data=file_data, fields=fields)

    def write_file(self, fpath, fields=None):
        """
        Rollup Meetup group data and write it to a file.
        """
        if fields is None:
            fields = self._fields
        with open(fpath, "w") as gfp:
            for gid in self._groups_data.get_gids():
                data = self._groups_data.lookup_gid(gid, fields=fields)
                print("{}".format(json.dumps(data)), file=gfp)

    def lookup_gid(self, gid, fields=None):
        """
        Return a dict containing Meetup group data for a gid.
        """
        if fields is None:
            fields = self._fields
        return self._groups_data.lookup_gid(gid, fields=fields)

    def get_gids(self):
        """
        Return the list of gids.
        """
        return self._groups_data.get_gids()


def gen_group_id_and_member_ids(stash_root):
    """
    The stash directory contains:
        stash/
            members_in_group_/
                1/2/12345.json
                1/2/12678.json
                ...
    This generator yields:
        12345, {"123", "124", "2345", ...}
        12678, {"567", "2345", ...}
    where 12345 is a group_id and the set contains the group member_ids
    """
    for group_id, fpath in gen_group_id_and_file_path(stash_root):
        member_ids = set()
        with open(fpath) as fin:
            for line in fin:
                data = json.loads(line)
                member_ids.add(str(data["member"]["id"]))
        yield group_id, member_ids


def gen_reduced_data(stash_root):
    """
    The stash directory contains:
        stash/
            members_in_group_/
                1/2/12345.json
                1/2/12678.json
                ...
    This generator yields JSON objects:
        {"gid": 12345, "gname": "a group", "mids": ["123", "2345", ...]}
        {"gid": 12678, "gname": "another group", "mids": ["23", "345", ...]}
    where mids is a list containing the group member_ids.
    """
    for gid, fpath in gen_group_id_and_file_path(stash_root):
        member_ids = set()
        with open(fpath) as fin:
            for line in fin:
                data = json.loads(line)
                member_ids.add(str(data["member"]["id"]))
        data = dict(
                gid=gid,
                group_name=group_name,
                members=list(member_ids),
                )
        yield json.dumps(data)


# A sample line from the json file for group_id 26434. The data downloaded
# using the MeetUp API is the dict with key "member" in this structure. It
# is embedded in another dict with contents {"n":2, "member":...,
# "group_id":"26434"}.
"""
{"n": 2, "member": {"link": "http://www.meetup.com/members/3259775", "id": 3259775, "state": "CA", "joined": 1199342891000, "topics": [], "self": {"common": {}}, "visited": 1449776819000, "name": "A. Karriem A.Khan", "lat": 37.83, "city": "Oakland", "photo": {"photo_link": "http://photos1.meetupstatic.com/photos/member/9/1/0/f/member_257497135.jpeg", "thumb_link": "http://photos1.meetupstatic.com/photos/member/9/1/0/f/thumb_257497135.jpeg", "photo_id": 257497135, "highres_link": "http://photos1.meetupstatic.com/photos/member/9/1/0/f/highres_257497135.jpeg"}, "hometown": "Silicon Bay", "status": "active", "other_services": {"twitter": {"identifier": "@ak2webd3"}, "facebook": {"identifier": "https://www.facebook.com/app_scoped_user_id/649887460/"}}, "country": "us", "lon": -122.26}, "group_id": "26434"}
"""
