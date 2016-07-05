#!/usr/bin/env python

import os
import sys

pwd = os.environ["PWD"]
progdir = os.path.dirname(sys.argv[0])
progdir_path = os.path.abspath(os.path.join(pwd, progdir))
print(progdir_path)
