#!/bin/sh
/usr/bin/setup-eth0.sh
/usr/bin/ioctl
/usr/bin/factorial $((1 << 28))
/bin/runtime-workload-elf /srv/workload
