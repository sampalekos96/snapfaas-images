mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

tesseract: compile_tesseract.sh
	echo "/srv/compile_tesseract.sh" | docker run -i --rm -v $(mkfile_path):/srv -w /tmp alpine:3.10

.PHONY: workload.java
workload.class:
	echo "apk add openjdk8 maven; mvn clean compile assembly:single; mv target/libworkload*.jar target/libworkload.jar" | docker run -i --rm -v $(mkfile_path):/app -w /app alpine:3.10

lib:
	test -d lib || mkdir lib

output.ext2: lib tesseract workload.class
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 200M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r lib tesseract target/libworkload.jar target/classes/srv/workload.class *.png /tmp/lorem.out/
	sudo umount /tmp/lorem.out/

.PHONY: clean
clean:
	sudo rm -r output.ext2 lib target tesseract
