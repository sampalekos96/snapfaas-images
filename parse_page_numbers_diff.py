#!/usr/bin/env python3

import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('files', help='comma-separated list of file names')
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
                sets[set_index].add(num[0])

kernel_sets = sets[0:3]
diff_sets = sets[3:6]
exec_sets = sets[6:9]

kernel_written_set = kernel_sets[0] - diff_sets[0]
diff_written_set = diff_sets[0]
exec_accessed_set = exec_sets[2]
#preexec_written_union = kernel_written_set | lang_written_set | func_written_set
#exec_kernel_intersection = exec_accessed_set & kernel_written_set
#exec_lang_intersection = exec_accessed_set & lang_written_set
#exec_func_intersection = exec_accessed_set & func_written_set
#exec_kernel_ro = exec_sets[1] & kernel_written_set
#exec_lang_ro = exec_sets[1] & lang_written_set
#exec_func_ro = exec_sets[1] & func_written_set
#exec_kernel_written = exec_sets[0] & kernel_written_set
exec_diff_accessed = exec_sets[2] & diff_written_set
#exec_func_written = exec_sets[0] & func_written_set

print('accessed/total ratio: {:.4f}'.format(len(exec_diff_accessed) / len(diff_written_set)))
#print("# of kernel pages: {}".format(len(kernel_written_set)))
#print("# of lang pages: {}".format(len(lang_written_set)))
#print("# of func pages: {}".format(len(func_written_set)))
#print("# of exec accessed pages: {}".format(len(exec_accessed_set)))
#print("***kernel pages***")
#print("# of kernel pages exec accessed: {}".format(len(exec_kernel_intersection)))
#print("# of kernel pages exec only read: {}".format(len(exec_kernel_ro)))
#print("# of kernel pages exec written: {}".format(len(exec_kernel_written)))
#with open(args.output_json[0], 'w') as outfile:
#    print(json.dumps(list(exec_kernel_intersection)), file=outfile)
#print("***lang pages***")
#print("# of lang pages exec accessed: {}".format(len(exec_lang_intersection)))
#print("# of lang pages exec only read: {}".format(len(exec_lang_ro)))
#print("# of lang pages exec written: {}".format(len(exec_lang_written)))
#with open(args.output_json[1], 'w') as outfile:
#    print(json.dumps(list(exec_lang_intersection)), file=outfile)
#print("***func pages***")
#print("# of func pages exec accessed: {}".format(len(exec_func_intersection)))
#print("# of func pages exec only read: {}".format(len(exec_func_ro)))
#print("# of func pages exec written: {}".format(len(exec_func_written)))
#print("***new pages***")
#print("# of new pages exec only read: {}".format(len(exec_sets[1] - exec_kernel_ro - exec_lang_ro - exec_func_ro)))
#print("# of new pages exec written: {}".format(len(exec_sets[0] - exec_kernel_written - exec_lang_written - exec_func_written)))
