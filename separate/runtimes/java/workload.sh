#!/usr/bin/env bash

/usr/bin/setup-eth0.sh
/usr/bin/ioctl

java bin.setup_java
java -cp ".:/bin/*:/srv/package/*" -Djava.library.path=/bin bin.runtime_workload
