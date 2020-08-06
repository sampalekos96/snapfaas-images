mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

package: workload requirements.txt
	test -d package || mkdir package
	echo "apk add musl-dev gcc zlib-dev jpeg-dev python3 python3-dev py3-pip; pip3 install --upgrade --target ./package -r requirements.txt" | docker run -i --rm -v $(mkfile_path):/app -w /app alpine:3.10

lib:
	test -d lib || mkdir lib
	echo "apk add jpeg zlib; cp -r /usr/lib/* /app/lib" | docker run -i --rm -v $(mkfile_path):/app -w /app alpine:3.10

output.ext2: package lib
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 150M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r *.jpg lib package workload /tmp/lorem.out/
	sudo umount /tmp/lorem.out

clean:
	sudo rm -r package
	sudo rm -r lib
	sudo rm output.ext2
