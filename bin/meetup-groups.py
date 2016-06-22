#!/usr/bin/env python3
"""
"""

import click
import json
import requests

default_payload = { 'status': 'past' }


def generate_groups(country_code, city_name, state_code, api_key):
    offset = 0
    while True:
        offset_payload = { 'offset': offset,
                           'key': api_key,
                           "country": country_code,
                           "city": city_name,
                           "state": state_code,
                           }
        #payload = default_payload.copy()
        #payload.update(offset_payload)
        # for Python 3.5: payload = {**default_payload, **offset_payload}
        payload = {**default_payload, **offset_payload}

        r = requests.get('https://api.meetup.com/2/groups', params=payload)
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


@click.command()
@click.option('--country', 'country_code', default='US', help='Country Code, i.e. US')
@click.option('--city', 'city_name', default='San Francisco', help='City name, i.e. San Francisco')
@click.option('--state', 'state_code', default='CA', help='State, i.e. CA')
@click.option('--apikey', 'api_key', envvar='MEETUP_API_KEY', help='Your Meetup.com API key, from https://secure.meetup.com/meetup_api/key/')
def go(country_code, city_name, state_code, api_key):

    all_groups = generate_groups(country_code, city_name, state_code, api_key)
    for group in all_groups:
        jdata = json.dumps(group)
        print("{}".format(jdata))

if __name__ == '__main__':
    go()
