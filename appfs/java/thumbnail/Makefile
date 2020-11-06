mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

.PHONY: workload.java
workload.class:
	echo "apk add openjdk8 maven; mvn clean compile assembly:single; mv target/libworkload*.jar target/libworkload.jar" | docker run -i --rm -v $(mkfile_path):/app -w /app alpine:3.10

lib: compile_imagemagick.sh
	test -d lib || mkdir lib
	echo "/srv/compile_imagemagick.sh" | docker run -i --rm -v $(mkfile_path):/srv -w /tmp alpine:3.10

output.ext2: lib workload.class
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 100M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r bin etc lib include share target/libworkload.jar target/classes/srv/workload.class *.jpg /tmp/lorem.out/
	sudo umount /tmp/lorem.out/

.PHONY: clean
clean:
	sudo rm -rf output.ext2 bin etc lib include share target
