mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

lib:
	test -d lib || mkdir lib

package: workload requirements.txt
	test -d package || mkdir -p package
	echo "apk add musl-dev python3 python3-dev py3-pip gcc; pip3 install --upgrade --target ./package -r requirements.txt; export PYTHONPATH=./package; export NLTK_DATA=./package/nltk_data; mkdir -p ./package/nltk_data; python3 -m textblob.download_corpora" | docker run -i --rm -v $(mkfile_path):/app -w /app alpine:3.10

output.ext2: lib package
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 300M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r lib package workload /tmp/lorem.out/
	sudo umount /tmp/lorem.out

clean:
	sudo rm -r package
	sudo rm -r lib
	sudo rm output.ext2
