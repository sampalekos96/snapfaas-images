mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

workload: workload.go
	echo "apk add go; cd /runtime; go mod download; go build -buildmode=plugin -o /runtime/workload" | docker run -i --rm -v $(mkfile_path):/runtime alpine

output.ext2: workload
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 10M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r workload go.mod go.sum workload.go /tmp/lorem.out/
	sudo umount /tmp/lorem.out/
