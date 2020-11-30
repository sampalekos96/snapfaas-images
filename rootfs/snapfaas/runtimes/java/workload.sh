#!/usr/bin/env bash

/usr/bin/setup-eth0.sh
/usr/bin/ioctl
factorial $((1 << 28))
java -jar /bin/RuntimeWorkload.jar
