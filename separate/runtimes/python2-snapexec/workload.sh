#!/usr/bin/env bash

do-snapshot 127
LD_LIBRARY_PATH=/srv python2 /bin/runtime-workload.py
