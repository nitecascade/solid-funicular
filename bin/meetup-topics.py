#!/usr/bin/env python3
"""
"""

import click
import json
import requests

default_payload = { 'status': 'past' }


def generate_topics(api_key):
    offset = 0
    while True:
        offset_payload = { 'offset': offset,
                           'key': api_key,
                           }
        #payload = default_payload.copy()
        #payload.update(offset_payload)
        # for Python 3.5: payload = {**default_payload, **offset_payload}
        payload = {**default_payload, **offset_payload}

        r = requests.get('https://api.meetup.com/2/topic_categories',
                params=payload)
        json = r.json()

        results, meta = json['results'], json['meta']
        for item in results:
            yield item

        # if we no longer have more results pages, stop…
        if not meta['next']:
            return

        offset = offset + 1


@click.command()
@click.option('--apikey', 'api_key', envvar='MEETUP_API_KEY', help='Your Meetup.com API key, from https://secure.meetup.com/meetup_api/key/')
def go(api_key):

    all_topics = generate_topics(api_key)
    for topic in all_topics:
        jdata = json.dumps(topic)
        print("{}".format(jdata))

if __name__ == '__main__':
    go()
