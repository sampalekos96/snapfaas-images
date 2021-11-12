#!/usr/bin/env python3

from importlib import import_module
import struct
import json
import time
import socket
import os
import sys
from subprocess import run, Popen

import syscalls_pb2

# vsock to communicate with the host
VSOCKPORT = 1234
sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
hostaddr = (socket.VMADDR_CID_HOST, VSOCKPORT)

app = import_module('workload')

class Syscall():
    def __init__(self, sock):
        self.sock = sock

    def write_key(self, key, value):
        req = syscalls_pb2.Syscall(writeKey = syscalls_pb2.WriteKey(key = key, value = value))
        reqData = req.SerializeToString()
        self.sock.sendall(struct.pack(">I", len(reqData)))
        self.sock.sendall(reqData)

        data = sock.recv(4, socket.MSG_WAITALL)
        res = struct.unpack(">I", data)
        responseData = sock.recv(res[0], socket.MSG_WAITALL)

        response = syscalls_pb2.WriteKeyResponse()
        response.ParseFromString(responseData)
        return response.success

    def read_key(self, key):
        req = syscalls_pb2.Syscall(readKey = syscalls_pb2.ReadKey(key = key))
        reqData = req.SerializeToString()
        self.sock.sendall(struct.pack(">I", len(reqData)))
        self.sock.sendall(reqData)

        data = sock.recv(4, socket.MSG_WAITALL)
        res = struct.unpack(">I", data)
        responseData = sock.recv(res[0], socket.MSG_WAITALL)

        response = syscalls_pb2.ReadKeyResponse()
        response.ParseFromString(responseData)
        return response.value

# send over the boot completion signal
for i in range(1, os.cpu_count()):
    Popen('taskset -c {} outl 123 0x3f0'.format(i), shell=True)
run('taskset -c 0 outl 123 0x3f0', shell=True)

sock.connect(hostaddr)
while True:
    sc = Syscall(sock)

    data = sock.recv(4, socket.MSG_WAITALL)
    res = struct.unpack(">I", data)
    requestData = sock.recv(res[0], socket.MSG_WAITALL)

    request = syscalls_pb2.Request()
    request.ParseFromString(requestData)

    start = time.monotonic_ns()
    resposneJson = {}
    try:
        responseJson = app.handle(json.loads(request.payload), sc)
    except:
        responseJson = { 'error': str(sys.exc_info()) }
    responseJson['duration'] = time.monotonic_ns() - start

    response = syscalls_pb2.Syscall(response = syscalls_pb2.Response(payload = json.dumps(responseJson)))

    responseData = response.SerializeToString()

    sock.sendall(struct.pack(">I", len(responseData)))
    sock.sendall(responseData)

