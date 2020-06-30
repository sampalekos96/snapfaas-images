#!/usr/bin/env bash
NCPU=$(grep -c ^processor /proc/cpuinfo)
for (( i = 1; i < $NCPU; i++ ))
do
    taskset -c $i outl 124 0x3f0 &
done
taskset -c 0 do-snapshot 126
LD_LIBRARY_PATH=/srv/lib python2 /bin/runtime-workload.py
