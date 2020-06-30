mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

lib:
	mkdir -p lib

dummy-carray:
	echo "apk add python2 python-dev gcc musl-dev; cd /app; python2 setup.py build" | docker run -i --rm -v $(mkfile_path)dummy-carray:/app -w /app alpine

package: dummy-carray
	mkdir -p package
	cp dummy-carray/build/lib.linux-x86_64-2.7/dummy_array.so package

output.ext2: lib package
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 10M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r package lib workload /tmp/lorem.out/
	sudo umount /tmp/lorem.out/
