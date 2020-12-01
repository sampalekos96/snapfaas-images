apk add bash git go musl-dev gcc build-base

go get -u golang.org/x/sys/unix

# Copy application over
cp -r /my-app/* /srv
cp -r /runtime/workload.go /srv/main.go

cd /srv/
CGO_ENABLED=1 go build -o /srv/workload
cd /

cp /runtime/workload.sh /bin/runtime-workload
chmod +x /bin/runtime-workload
