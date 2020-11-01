mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

lib: compile_chromaprint.sh
	test -d lib || mkdir lib
	echo "/srv/compile_chromaprint.sh" | docker run -i --rm -v $(mkfile_path):/srv -w /tmp alpine:3.10

package: requirements.txt
	test -d package || mkdir package
	echo "apk add python3 py3-pip python3-dev; pip3 install --upgrade --target ./package -r requirements.txt" | docker run -i --rm -v $(mkfile_path):/app -w /app alpine:3.10

__pycache__: workload.py package
	echo "apk add python3; PYTHONPATH=/app:/app/package python3 -m workload" | docker run -i --rm -v $(mkfile_path):/app -w /app alpine:3.10

output.ext2: lib package __pycache__
	sudo rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 200M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r *.wav package bin lib workload.py __pycache__ /tmp/lorem.out/
	sudo umount /tmp/lorem.out/

clean:
	sudo rm -rf package
	sudo rm -rf lib
	sudo rm -rf bin
	sudo rm -rf include
	sudo rm -f output.ext2
	sudo rm -rf __pycache__
