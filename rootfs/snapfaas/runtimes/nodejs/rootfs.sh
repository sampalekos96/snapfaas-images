apk add nodejs npm python make g++ linux-headers

npm install -g --unsafe-perm $(npm pack /runtime/vsock | tail -1)

cp /runtime/workload.js /bin/runtime-workload.js
cp /runtime/workload.sh /bin/runtime-workload
chmod +x /bin/runtime-workload

apk del npm python make g++ linux-headers

cp /common/factorial /usr/bin/factorial
