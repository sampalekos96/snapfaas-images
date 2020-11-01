#!/usr/bin/env python3

from importlib import import_module
import os
import struct
import json
from subprocess import run, Popen
import time
import socket

# vsock to communicate with the host
VSOCKPORT = 1234
sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
hostaddr = (socket.VMADDR_CID_HOST, VSOCKPORT)

app = import_module('workload')

# for function snapshot
for i in range(1, os.cpu_count()):
    Popen('taskset -c %d outl 124 0x3f0'%(i), shell=True)
run('taskset -c 0 outl 124 0x3f0', shell=True)

sock.connect(hostaddr)
while True:
    data = sock.recv(4, socket.MSG_WAITALL)
    res = struct.unpack(">I", data)
    requestJson = sock.recv(res[0], socket.MSG_WAITALL).decode("utf-8")

    request = json.loads(requestJson)

    start = time.monotonic_ns()
    response = app.handle(request)
    response['duration'] = time.monotonic_ns() - start

    responseJson = json.dumps(response)

    sock.sendall(struct.pack(">I", len(responseJson)))
    sock.sendall(bytes(responseJson, "utf-8"))
