mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: workload.class output.ext2

workload.class:
	javac -cp ".:../.package/*" workload.java

output.ext2:
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 10M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r workload.class /tmp/lorem.out/
	sudo umount /tmp/lorem.out/
