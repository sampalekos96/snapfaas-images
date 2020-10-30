apk add nodejs npm python make g++ linux-headers

npm install -g --unsafe-perm $(npm pack /runtime/vsock | tail -1)

apk del npm python make g++ linux-headers

# Copy application over
cp -r /my-app/* /srv

cp /runtime/workload.js /bin/runtime-workload.js

cp /common/factorial /usr/bin/factorial
