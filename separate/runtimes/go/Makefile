mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: workload

workload: workload.go
	echo "apk add git go; go get -u golang.org/x/sys/unix; go build -o /runtime/workload /runtime/workload.go" | docker run -i --rm -v $(mkfile_path):/runtime alpine
