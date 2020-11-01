#!/usr/bin/env bash

/usr/bin/setup-eth0.sh
/usr/bin/ioctl

java -jar /bin/RuntimeWorkload.jar
