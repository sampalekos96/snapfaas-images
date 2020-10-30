#!/usr/bin/env bash

/usr/bin/setup-eth0.sh
/usr/bin/ioctl
LD_LIBRARY_PATH=/srv/lib PYTHONPATH=/srv/package python3 /bin/runtime-workload.py
