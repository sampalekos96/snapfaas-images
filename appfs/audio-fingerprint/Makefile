mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

lib:
	mkdir lib

chromaprint: lib compile_chromaprint.sh
	echo "/srv/compile_chromaprint.sh" | docker run -i --rm -v $(mkfile_path):/srv -w /tmp alpine:3.10


package: workload requirements.txt
	mkdir package
	echo "apk add python3 py3-pip python3-dev; pip3 install --upgrade --target ./package -r requirements.txt; export PYTHONPATH=./package" | docker run -i --rm -v $(mkfile_path):/app -w /app alpine:3.10

output.ext2: chromaprint package
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 200M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r *.wav *.raw package lib workload /tmp/lorem.out/
	sudo umount /tmp/lorem.out/
