apk add git go build-base

go get -u golang.org/x/sys/unix
go build -o /bin/runtime-workload-elf /runtime/workload.go
chmod +x /bin/runtime-workload-elf

cp /common/factorial /usr/bin/factorial

apk del git go build-base
