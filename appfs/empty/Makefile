mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

output.ext2:
	rm -rf output.ext2
	touch output.ext2
	truncate -s 500M output.ext2
	mkfs.ext2 output.ext2
