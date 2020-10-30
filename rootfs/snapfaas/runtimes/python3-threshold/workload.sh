#!/usr/bin/env bash

/usr/bin/setup-eth0.sh
/usr/bin/ioctl
outl 124 0x3f0
LD_LIBRARY_PATH=/srv/lib python3 /bin/runtime-workload.py
