mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

tesseract: compile_tesseract.sh
	echo "/srv/compile_tesseract.sh" | docker run -i --rm -v $(mkfile_path):/srv -w /tmp alpine:3.10

lib:
	mkdir -p lib

package:
	mkdir package

output.ext2: package lib tesseract
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 200M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r lib package tesseract workload *.png *.jpg /tmp/lorem.out/
	sudo umount /tmp/lorem.out/
