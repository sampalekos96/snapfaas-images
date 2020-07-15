mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

lib:
	mkdir -p lib

dummy-carray:
	echo "apk add python3 python3-dev gcc musl-dev; cd /app; python3 setup.py build" | docker run -i --rm -v $(mkfile_path)../dummy-carray:/app -w /app alpine:3.10

package: dummy-carray
	mkdir -p package
	cp ../dummy-carray/build/lib.linux-x86_64-3.7/dummy_array.cpython-37m-x86_64-linux-gnu.so package/dummy_array.so

output.ext2: lib package
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 10M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r package lib workload /tmp/lorem.out/
	sudo umount /tmp/lorem.out/
