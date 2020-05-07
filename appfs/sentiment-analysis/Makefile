mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

package: workload requirements.txt
	mkdir -p package
	echo "apk add musl-dev python2 python2-dev py2-pip gcc; pip2 install --upgrade --target ./package -r requirements.txt; export PYTHONPATH=./package; export NLTK_DATA=./package/nltk_data; mkdir -p ./package/nltk_data; python -m textblob.download_corpora lite" | docker run -i --rm -v $(mkfile_path):/app -w /app alpine

output.ext2: package
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 150M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r package workload declaration.json /tmp/lorem.out/
	sudo umount /tmp/lorem.out
