#!/usr/bin/env python3

import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('files', help='comma-separated list of file names')
args = parser.parse_args()

sets = []
set_index = -1

for fname in args.files.split(','):
    with open(fname) as infile:
        lines = infile.readlines()
        assert(len(lines) == 1)
        sets.append(set(json.loads(lines[0])))

assert(len(sets) >= 2)
common_set = sets[0]
for i in range(len(sets) - 1):
    common_set &= sets[i+1]

print("# of common pages exec accessed: {}".format(len(common_set)))
