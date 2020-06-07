mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

package: requirements.txt
	mkdir -p package
	echo "apk add musl-dev gcc zlib-dev jpeg-dev python2 python2-dev py2-pip; pip2 install --upgrade --target ./package -r requirements.txt" | docker run -i --rm -v $(mkfile_path):/app -w /app alpine

library:
	echo "apk add jpeg zlib; cp /usr/lib/libjpeg* /app" | docker run -i --rm -v $(mkfile_path):/app -w /app alpine

output.ext2: workload package library
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 150M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r libjpeg* *.jpg package workload /tmp/lorem.out/
	sudo umount /tmp/lorem.out
