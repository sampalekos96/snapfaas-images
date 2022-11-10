#!/usr/bin/env bash

/usr/bin/setup-eth0.sh
/usr/bin/ioctl
#/usr/bin/virt_to_phys_user pid 1073754112
factorial $((1 << 28))
LD_LIBRARY_PATH=/srv/lib PYTHONPATH=/srv:/srv/package python3 /bin/runtime-workload.py
