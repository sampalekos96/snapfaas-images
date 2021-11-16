apk add bash python3 python3-dev

# Copy application over
cp -r /my-app/* /srv

cp -r /runtime/google /usr/lib/python3.7/google
cp /runtime/workload.py /bin/runtime-workload.py
cp /runtime/syscalls_pb2.py /usr/lib/python3.7/syscalls_pb2.py
