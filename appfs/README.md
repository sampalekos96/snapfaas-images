The `empty` directory contains a 500MiB empty `.ext4` file for users to generate snapshots with.

All the other directories are applications. An application directory should contain an entry script
named `workload` which should define the entry function `handle` and a dependency description file
(e.g. requirements.txt for python and package.json for Node.js). The directory should also includes
a `Makefile` to generate the application file system the `output.ext2` file.
