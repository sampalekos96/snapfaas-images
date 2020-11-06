mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: workload.class output.ext2

.PHONY: workload.java
workload.class:
	echo "apk add openjdk8 maven; mvn clean compile assembly:single; mv target/libworkload*.jar target/libworkload.jar" | docker run -i --rm -v $(mkfile_path):/app -w /app alpine:3.10

output.ext2:
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 10M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r target/libworkload.jar target/classes/srv/workload.class *.jpg /tmp/lorem.out/
	sudo umount /tmp/lorem.out/

.PHONY: clean
clean:
	sudo rm -rf output.ext2 target
