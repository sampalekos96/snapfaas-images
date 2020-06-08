mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

tesseract: compile_tesseract.sh
	echo "/srv/compile_tesseract.sh" | docker run -i --rm -v $(mkfile_path):/srv -w /tmp alpine

lib:
	mkdir -p lib

output.ext2: lib tesseract
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 200M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r tesseract workload *.png *.jpg /tmp/lorem.out/
	sudo umount /tmp/lorem.out/
