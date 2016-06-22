#!/usr/bin/env python3

import json
import pprint
import sys

infile = sys.argv[1]

with open(infile) as fp:
    for line in fp:
        data = json.loads(line.strip())
        print("{id} {name}".format(**data))
        #print(pprint.pformat(data))
