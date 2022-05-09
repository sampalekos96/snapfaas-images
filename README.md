SnapFaaS uses `docker` to build both kinds of filesystems.
The Linux distro used is Alpine Linux v3.10.

## root filesystem

Currently Python3.7 and Node.js10 are supported. To build a root filesystem, execute

```bash
cd snapfaas-images/separate
# replace the path `/ssd/rootfs/python3.ext4` with the path at which you want to place the root filesystem.
./mk_rt_images [python3|nodejs] /ssd/rootfs/[python3|nodejs].ext4
```

## application filesystem

```bash
# use hello as example
cd snapfaas-images/appfs/hellopy2
make
```

The command above generates `output.ext2` in the `hellopy2` directory.

## rootfs
`rootfs` contains four subdirectories, namely `common`, `fullapp`, `regular`, and `snapfaas`.

Directory `common` contain files that are common to the rest three directories each of which represents
a style of booting a guest VM.

Directory `fullapp` contains code and scripts to generate root file systems each of which contains
**both** a language runtime and an application. All wrapper scripts contain one snapshotting point.

Directory `regular` contains code and scripts to generate root file systems each of which contains
**both** a language runtime and an application. The **difference** between `regular` and `fullapp`
is that `regular` runtime wrapper scripts contain no snapshotting point. Otherwise, the two
are the same.

Directory `snapfaas` contains code and scripts to generate root file systems each of which contains
just one language runtime and **no** application code. `snapfaas` runtime wrapper scripts expects
a second file system, i.e. appfs, which contains application code and mounts it to `/srv`. All wrapper
scripts contain two snapshotting point. The first is for generating language snapshot and the second
is for generating diff snapshot.

**Note** that `snapfaas` contains some special runtimes that are only intended for special measurements.
See `snapfaas/README.md`.

## appfs
Directory `appfs` contains serverless functions:
1. Python3 functions are under `appfs/python3`.
2. Node.js functions are under `appfs/nodejs`.

Each directory in `appfs/$runtime` is a serverless function containing files and a `Makefile` to build
the filesystem for the function.

Each app directory that begins with "." are apps that snapfaas/microbenchmark will skip.
