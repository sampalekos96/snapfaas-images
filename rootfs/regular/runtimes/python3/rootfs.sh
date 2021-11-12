apk add bash python3 python3-dev

# Copy application over
cp -r /my-app/* /srv

cp -r /runtime/google /bin/google
cp /runtime/workload.py /bin/runtime-workload.py
cp /runtime/syscalls_pb2.py /bin/syscalls_pb2.py
