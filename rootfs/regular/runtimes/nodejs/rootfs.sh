apk add nodejs npm python make g++ linux-headers

npm install -g --unsafe-perm $(npm pack /runtime/vsock | tail -1)

apk del npm python make g++ linux-headers

# Copy application over
cp -r /my-app/* /srv

cp /runtime/workload.js /bin/runtime-workload.js

## Create start script for that mounts the appfs and invokes whatever binary is in /srv/workload
cat /runtime/workload.sh > /bin/workload
chmod +x /bin/workload

## Have the start script invoked by openrc/init
printf '#!/sbin/openrc-run\n
command="/bin/workload"\n' > /etc/init.d/serverless-workload
chmod +x /etc/init.d/serverless-workload
rc-update add serverless-workload default
