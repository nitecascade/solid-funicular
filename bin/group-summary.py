#!/usr/bin/env python3

import json
import pprint
import sys

infile = sys.argv[1]

with open(infile) as fp:
    for line in fp:
        data = json.loads(line.strip())
        member = data["member"]
        try:
            print("{id} {name!r}".format(**member))
        except KeyError as exc:
            print("KeyError: {}".format(exc))
            print(pprint.pformat(data))
