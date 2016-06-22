#!/usr/bin/env python3
"""
"""

import click
import json
import requests
import time
from pprint import pformat

default_payload = { 'status': 'past' }


def generate_member_group(member_id, api_key, sleep=None):
    offset = 0
    while True:
        offset_payload = { 'offset': offset,
                           'key': api_key,
                           "member_id": member_id,
                           }
        #payload = default_payload.copy()
        #payload.update(offset_payload)
        # for Python 3.5: payload = {**default_payload, **offset_payload}
        payload = {**default_payload, **offset_payload}

        r = requests.get('https://api.meetup.com/2/members', params=payload)
        if r.status_code != 200:
            print("status: {}".format(r.status_code))
            break

        json = r.json()
        results, meta = json['results'], json['meta']

        for item in results:
            yield item

        # if we no longer have more results pages, stop…
        if not meta['next']:
            return

        offset = offset + 1
        if sleep is not None:
            time.sleep(sleep)


@click.command()
@click.option('--group-id', 'group_id', default=None, help='Group_id')
@click.option('--apikey', 'api_key', envvar='MEETUP_API_KEY', help='Your Meetup.com API key, from https://secure.meetup.com/meetup_api/key/')
def go(group_id, api_key):

    all_members_in_group = generate_members_in_group(group_id, api_key)
    member_list = []
    for member in all_members_in_group:
        print(">> {}".format(pformat(member)))
        member_list.append(member)
    jdata = json.dumps(member_list)
    print("{}".format(jdata))

if __name__ == '__main__':
    go()
