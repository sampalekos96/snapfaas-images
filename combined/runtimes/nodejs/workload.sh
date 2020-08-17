#!/usr/bin/env sh

/usr/bin/setup-eth0.sh
/usr/bin/ioctl
NODE_PATH=$NODE_PATH:/usr/lib/node_modules node /bin/runtime-workload.js
