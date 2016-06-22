#!/usr/bin/env python3
"""
"""

import click
import json
import requests

default_payload = { 'status': 'past' }


def generate_cities(api_key):
    offset = 0
    while True:
        offset_payload = { 'offset': offset,
                           'key': api_key,
                           }
        #payload = default_payload.copy()
        #payload.update(offset_payload)
        # for Python 3.5: payload = {**default_payload, **offset_payload}
        payload = {**default_payload, **offset_payload}

        r = requests.get('https://api.meetup.com/2/cities', params=payload)
        json = r.json()

        try:
            results, meta = json['results'], json['meta']
        except Exception as exc:
            print(exc)
        else:
            for item in results:
                yield item

        # if we no longer have more results pages, stop…
        if not meta['next']:
            return

        offset = offset + 1


@click.command()
@click.option('--apikey', 'api_key', envvar='MEETUP_API_KEY', help='Your Meetup.com API key, from https://secure.meetup.com/meetup_api/key/')
def go(api_key):

    all_cities = generate_cities(api_key)
    for city in all_cities:
        jdata = json.dumps(city)
        print("{}".format(jdata))

if __name__ == '__main__':
    go()
