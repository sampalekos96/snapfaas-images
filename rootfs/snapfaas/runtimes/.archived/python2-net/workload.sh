#!/usr/bin/env bash

/usr/bin/setup-eth0.sh
LD_LIBRARY_PATH=/srv/lib python2 /bin/runtime-workload.py
