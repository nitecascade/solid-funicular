#!/usr/bin/env python3
"""
"""

import click
import json
import os
from pprint import pformat
import requests
import time
import sys

default_payload = { 'status': 'past' }


def generate_members_in_group(group_id, api_key, sleep=None):
    offset = 0
    while True:
        offset_payload = { 'offset': offset,
                           'key': api_key,
                           "group_id": group_id,
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
@click.argument('output-file', type=click.Path())
def go(group_id, api_key, output_file):
    if output_file != "-" and os.path.exists(output_file):
        click.echo("file exists: {!r}".format(output_file))
        click.echo("remove it first")
        sys.exit(1)
    all_members_in_group = generate_members_in_group(group_id, api_key)
    n = 0
    with click.open_file(output_file, "w") as outf:
        for member in all_members_in_group:
            n += 1
            if n % 10 == 0:
                print("{}".format("."), end="", flush=True, file=sys.stderr)
            if n % 1000 == 0:
                print("\n{}".format(n), flush=True, file=sys.stderr)
            jobj = dict(group_id=group_id, n=n, member=member)
            jdata = json.dumps(jobj)
            print("{}".format(jdata), flush=True, file=outf)
        print("\n{}".format(n), flush=True, file=sys.stderr)

if __name__ == '__main__':
    go()
