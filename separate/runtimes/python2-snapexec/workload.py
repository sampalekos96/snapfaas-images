#!/usr/bin/env python2

import sys
import imp
import struct
import json
from subprocess import call, Popen
import multiprocessing as mp
import time

with open('/dev/ttyS1', 'r') as tty, open('/dev/ttyS1', 'w') as out:
    # for language snapshot
    for i in range(1, mp.cpu_count()):
        Popen('taskset -c %d outl 124 0x3f0'%(i), shell=True)
    call('taskset -c 0 do-snapshot 123', shell=True)

    call(["mount", "-r", "/dev/vdb", "/srv"], executable="/bin/mount")

    sys.path.append('/srv/package')
    app = imp.load_source('app', '/srv/workload')

    # for function diff snapshot
    for i in range(1, mp.cpu_count()):
        Popen('taskset -c %d outl 124 0x3f0'%(i), shell=True)
    call('taskset -c 0 do-snapshot 126', shell=True)

    while True:
        request = json.loads(tty.readline())

        response = app.handle(request)

        responseJson = json.dumps(response)

        out.write(struct.pack(">I", len(responseJson)))
        out.write(bytes(responseJson))
        out.flush()
        # exec snapshot
        for i in range(1, mp.cpu_count()):
            Popen('taskset -c %d outl 124 0x3f0'%(i), shell=True)
        call('taskset -c 0 do-snapshot 126', shell=True)
