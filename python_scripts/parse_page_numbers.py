#!/usr/bin/env python3

import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('files', help='comma-separated list of `page_numbers` files generated during snapshot creation')
args = parser.parse_args()

sets = []
set_index = -1

for fname in args.files.split(','):
    with open(fname) as infile:
        for line in infile:
            num = line.strip().split(' ')
            if len(num) > 1:
                set_index += 1
                sets.append(set())
            else:
                sets[set_index].add(int(num[0]))

STEP = 3
sliced_sets = []
for i in range(len(sets)//3-1):
    i = i * STEP;
    sliced_sets.append(sets[i:i+STEP])
exec_sets = sets[len(sets)-3:]

written_sets = []
for i in range(len(sliced_sets)):
    written_set = sliced_sets[i][0]
    for j in range(1, len(sliced_sets)-i):
        written_set -= sliced_sets[j][0]
    written_sets.append(written_set)

exec_accessed_sets = []
exec_accessed_set = exec_sets[2]
for i in range(len(sliced_sets)):
    exec_accessed_sets.append(exec_sets[2] & written_sets[i])

exec_ro_sets = []
for i in range(len(sliced_sets)):
    exec_ro_sets.append(exec_sets[1] & written_sets[i])

exec_wr_sets = []
for i in range(len(sliced_sets)):
    exec_wr_sets.append(exec_sets[0] & written_sets[i])

accessed_pages = 0
total_pages = 0
print("total # of pages execution accessed:", len(exec_accessed_set))
for i in range(len(sliced_sets)):
    print('+++++PHASE', i+1)
    print("# of pages initialized:", len(written_sets[i]))
    print("# of pages execution accessed:", len(exec_accessed_sets[i]))
    print("# of pages execution only read:", len(exec_ro_sets[i]))
    print("# of pages execution wrote:", len(exec_wr_sets[i]))
    print('ratio of accessed over initialized:', len(exec_accessed_sets[i])/len(written_sets[i]))
    total_pages += len(written_sets[i])
    accessed_pages += len(exec_accessed_sets[i])
print('ratio of overall accessed over overall initialized:', accessed_pages/total_pages)
print("***new pages***")
ro = exec_sets[1]
for i in range(len(sliced_sets)):
    ro -= exec_ro_sets[i]
wr = exec_sets[0]
for i in range(len(sliced_sets)):
    ro -= exec_wr_sets[i]
print("# of new pages execution accessed:", len(wr)+len(ro))
print("# of new pages execution only read:", len(ro))
print("# of new pages execution wrote:", len(wr))
