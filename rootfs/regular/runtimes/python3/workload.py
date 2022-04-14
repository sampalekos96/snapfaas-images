#!/usr/bin/env python3

from importlib import import_module
import struct
import json
import time
import socket
import os
import sys
import traceback
from subprocess import run, Popen

import syscalls_pb2

# vsock to communicate with the host
VSOCKPORT = 1234
sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
hostaddr = (socket.VMADDR_CID_HOST, VSOCKPORT)

app = import_module('workload')

def sendall(sock, data):
    totalsent = 0
    while totalsent < len(data):
        sent = sock.send(data[totalsent:(totalsent+1024)])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

class Syscall():
    def __init__(self, sock):
        self.sock = sock

    def _send(self, req):
        reqData = req.SerializeToString()
        lenBuf = struct.pack(">I", len(reqData))
        self.sock.sendall(lenBuf)
        sendall(self.sock, reqData)

    def _recv(self, response):
        data = sock.recv(4, socket.MSG_WAITALL)
        res = struct.unpack(">I", data)
        responseData = recvall(self.sock, res[0])

        response.ParseFromString(responseData)
        return response

    def write_key(self, key, value):
        req = syscalls_pb2.Syscall(writeKey = syscalls_pb2.WriteKey(key = key, value = value))
        self._send(req)
        response = self._recv(syscalls_pb2.WriteKeyResponse())
        return response.success

    def read_key(self, key):
        req = syscalls_pb2.Syscall(readKey = syscalls_pb2.ReadKey(key = key))
        self._send(req)
        response = self._recv(syscalls_pb2.ReadKeyResponse())
        return response.value

    def get_current_label(self):
        req = syscalls_pb2.Syscall(getCurrentLabel = syscalls_pb2.GetCurrentLabel())
        self._send(req)
        response = self._recv(syscalls_pb2.DcLabel())
        return response

    def taint(self, label):
        req = syscalls_pb2.Syscall(taintWithLabel = label)
        self._send(req)
        response = self._recv(syscalls_pb2.DcLabel())
        return response

    def github_rest_get(self, route):
        req = syscalls_pb2.Syscall(githubRest = syscalls_pb2.GithubRest(verb = syscalls_pb2.HttpVerb.GET, route = route, body = None))
        self._send(req)
        response= self._recv(syscalls_pb2.GithubRestResponse())
        return response

    def github_rest_post(self, route, body):
        bodyJson = json.dumps(body)
        req = syscalls_pb2.Syscall(githubRest = syscalls_pb2.GithubRest(verb = syscalls_pb2.HttpVerb.POST, route = route, body = bodyJson))
        self._send(req)
        response= self._recv(syscalls_pb2.GithubRestResponse())
        return response

    def github_rest_put(self, route, body):
        bodyJson = json.dumps(body)
        req = syscalls_pb2.Syscall(githubRest = syscalls_pb2.GithubRest(verb = syscalls_pb2.HttpVerb.PUT, route = route, body = bodyJson))
        self._send(req)
        response= self._recv(syscalls_pb2.GithubRestResponse())
        return response

    def github_rest_delete(self, route, body):
        bodyJson = json.dumps(body)
        req = syscalls_pb2.Syscall(githubRest = syscalls_pb2.GithubRest(verb = syscalls_pb2.HttpVerb.DELETE, route = route, body = bodyJson))
        self._send(req)
        response= self._recv(syscalls_pb2.GithubRestResponse())
        return response

    def invoke(self, function, payload):
        req = syscalls_pb2.Syscall(invoke = syscalls_pb2.Invoke(function = function, payload = payload))
        self._send(req)
        response= self._recv(syscalls_pb2.InvokeResponse())
        return response.success

    def fswrite(self, path, data):
        req = syscalls_pb2.Syscall(fsWrite = syscalls_pb2.FSWrite(path = path, data = data))
        self._send(req)
        response = self._recv(syscalls_pb2.WriteKeyResponse())
        return response.success

    def fsread(self, path):
        req = syscalls_pb2.Syscall(fsRead = syscalls_pb2.FSRead(path = path))
        self._send(req)
        response = self._recv(syscalls_pb2.ReadKeyResponse())
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
    try:
        response = app.handle(json.loads(request.payload), sc)
        response['duration'] = time.monotonic_ns() - start
        # return value from Lambda can be not JSON serializable
        response = syscalls_pb2.Syscall(response = syscalls_pb2.Response(payload = json.dumps(response)))
    except:
        ty, val, tb = sys.exc_info()
        response = {
            'error': {
                'type': str(ty),
                'value': str(val),
                'traceback': traceback.format_tb(tb),
            },
        }
        response['duration'] = time.monotonic_ns() - start
        response = syscalls_pb2.Syscall(response = syscalls_pb2.Response(payload = json.dumps(response)))

    responseData = response.SerializeToString()

    sock.sendall(struct.pack(">I", len(responseData)))
    sendall(sock, responseData)

