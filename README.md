Directory `combined` contains code and scripts to generate root file systems each of which contain
**both** a language runtime and an application.

Directory `separate` contains code and scripts to generate root file systems each of which contain
just one language runtime. The root file system contains a wrapper of the langauge that expects a
second file system which contains an application.

Directory `appfs` contains serverless functions:
1. Python3 functions are under `appfs/python3`.
2. Node.js functions are under `appfs/nodejs`.

Each directory in `appfs/$runtime` is a serverless function containing files and a `Makefile` to build
the filesystem for the function.

Each app directory that begins with "." are apps that snapfaas/microbenchmark will skip.
