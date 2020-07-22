mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

package: workload requirements.txt
	mkdir -p package
	echo "apk add python2 python2-dev py2-pip; pip2 install --target ./package -r requirements.txt" | docker run -i --rm -v $(mkfile_path):/app -w /app alpine

output.ext2: package
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 10M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r package workload README /tmp/lorem.out/
	sudo umount /tmp/lorem.out/
