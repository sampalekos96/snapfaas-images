#!/usr/bin/env python3

from importlib import import_module
import struct
import json
import time
import socket

# vsock to communicate with the host
VSOCKPORT = 1234
sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
hostaddr = (socket.VMADDR_CID_HOST, VSOCKPORT)

app = import_module('workload')

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
