#!/usr/bin/env python3

import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('files', help='comma-separated list of `page_numbers` files generated during snapshot creation')
#parser.add_argument('--output_json', nargs=2, help='file that contains the set of page numbers a function execution accesses that are in the language snapshot', required=True)
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
#kernel_sets = sets[0:3]
#lang_sets = sets[3:6]
#func_sets = sets[6:9]

written_sets = []
for i in range(len(sliced_sets)):
    written_set = sliced_sets[i][0]
    for j in range(1, len(sliced_sets)-i):
        written_set -= sliced_sets[j][0]
    written_sets.append(written_set)
#kernel_written_set = kernel_sets[0] - lang_sets[0] - func_sets[0]
#lang_written_set = lang_sets[0] - func_sets[0]
#func_written_set = func_sets[0]
#preexec_written_union = kernel_written_set | lang_written_set | func_written_set

exec_accessed_sets = []
exec_accessed_set = exec_sets[2]
for i in range(len(sliced_sets)):
    exec_accessed_sets.append(exec_sets[2] & written_sets[i])
    #exec_kernel_intersection = exec_accessed_set & kernel_written_set
    #exec_lang_intersection = exec_accessed_set & lang_written_set
    #exec_func_intersection = exec_accessed_set & func_written_set

exec_ro_sets = []
for i in range(len(sliced_sets)):
    exec_ro_sets.append(exec_sets[1] & written_sets[i])
#exec_kernel_ro = exec_sets[1] & kernel_written_set
#exec_lang_ro = exec_sets[1] & lang_written_set
#exec_func_ro = exec_sets[1] & func_written_set

exec_wr_sets = []
for i in range(len(sliced_sets)):
    exec_wr_sets.append(exec_sets[0] & written_sets[i])
#exec_kernel_written = exec_sets[0] & kernel_written_set
#exec_lang_written = exec_sets[0] & lang_written_set
#exec_func_written = exec_sets[0] & func_written_set

accessed_pages = 0
total_pages = 0
print("total # of exec accessed pages: {}".format(len(exec_accessed_set)))
for i in range(len(sliced_sets)):
    print("# of pages initialized during phase {}: {}".format(i + 1, len(written_sets[i])))
    print("# of pages exec accessed:", len(exec_accessed_sets[i]))
    print("# of pages exec only read:", len(exec_ro_sets[i]))
    print("# of pages exec wrote:", len(exec_wr_sets[i]))
    print('ratio of pages accessed:', len(exec_accessed_sets[i])/len(written_sets[i]))
    total_pages += len(written_sets[i])
    accessed_pages += len(exec_accessed_sets[i])
print('ratio of pages accessed over total:', accessed_pages/total_pages)
print("***new pages***")
ro = exec_sets[1]
for i in range(len(sliced_sets)):
    ro -= exec_ro_sets[i]
wr = exec_sets[0]
for i in range(len(sliced_sets)):
    ro -= exec_wr_sets[i]
print("# of new pages exec only read:", len(ro))
print("# of new pages exec wrote:", len(wr))
#print("***lang pages***")
#print("# of lang pages exec accessed: {}".format(len(exec_lang_intersection)))
#print("# of lang pages exec only read: {}".format(len(exec_lang_ro)))
#print("# of lang pages exec written: {}".format(len(exec_lang_written)))
#print("***func pages***")
#print("# of func pages exec accessed: {}".format(len(exec_func_intersection)))
#print("# of func pages exec only read: {}".format(len(exec_func_ro)))
#print("# of func pages exec written: {}".format(len(exec_func_written)))
#with open(args.output_json[0], 'w') as outfile:
#    print(json.dumps(list(exec_kernel_intersection)), file=outfile)
#with open(args.output_json[1], 'w') as outfile:
#    print(json.dumps(list(exec_lang_intersection)), file=outfile)
