#!/usr/bin/env python3

import json
import os
from pprint import pformat
import sys

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

# A sample line from the json file for group_id 26434. The data downloaded
# using the MeetUp API is the dict with key "member" in this structure. It
# is embedded in another dict with contents {"n":2, "member":...,
# "group_id":"26434"}.
"""
{"n": 2, "member": {"link": "http://www.meetup.com/members/3259775", "id": 3259775, "state": "CA", "joined": 1199342891000, "topics": [], "self": {"common": {}}, "visited": 1449776819000, "name": "A. Karriem A.Khan", "lat": 37.83, "city": "Oakland", "photo": {"photo_link": "http://photos1.meetupstatic.com/photos/member/9/1/0/f/member_257497135.jpeg", "thumb_link": "http://photos1.meetupstatic.com/photos/member/9/1/0/f/thumb_257497135.jpeg", "photo_id": 257497135, "highres_link": "http://photos1.meetupstatic.com/photos/member/9/1/0/f/highres_257497135.jpeg"}, "hometown": "Silicon Bay", "status": "active", "other_services": {"twitter": {"identifier": "@ak2webd3"}, "facebook": {"identifier": "https://www.facebook.com/app_scoped_user_id/649887460/"}}, "country": "us", "lon": -122.26}, "group_id": "26434"}
"""
