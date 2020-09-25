mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: workload.class output.ext2

.PHONY: workload.java
workload.class:
	echo "apk add openjdk8; /usr/lib/jvm/java-1.8-openjdk/bin/javac -cp \".:package/*:../.package/*\" workload.java" | docker run -i --rm -v $(mkfile_path):/app -w /app alpine:3.10

output.ext2:
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 10M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r package workload.class /tmp/lorem.out/
	sudo umount /tmp/lorem.out/

.PHONY: clean
clean:
	rm -f output.ext2 rm workload.class
