#!/usr/bin/env bash

/usr/bin/setup-eth0.sh
/usr/bin/ioctl
factorial $((1 << 28))
LD_LIBRARY_PATH=/srv/lib python3 /bin/runtime-workload.py
