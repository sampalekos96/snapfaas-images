#!/usr/bin/env bash

/usr/bin/setup-eth0.sh
/usr/bin/ioctl

java -cp ".:/bin:/lib/json-simple-1.1.1.jar:/lib/VSock.jar" RuntimeWorkload
