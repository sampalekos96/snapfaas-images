mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

node_modules: package.json workload
	[ -d 'node_modules' ] && rm -r node_modules || true
	mkdir node_modules
	echo "apk add nodejs npm; npm install" | docker run -i --rm -v $(mkfile_path):/app -w /app alpine

output.ext2: node_modules
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 10M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r node_modules workload README /tmp/lorem.out/
	sudo umount /tmp/lorem.out/
