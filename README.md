Directory `combined` contains code and scripts to generate root file systems each of which contain
**both** a language runtime and an application.

Directory `separate` contains code and scripts to generate root file systems each of which contain
just one language runtime. The root file system contains a wrapper of the langauge that expects a
second file system which contains an application.

Directory `appfs` contains serverless functions. All Python3 functions are under `appfs/python3`.
Each directory in `appfs/python3` is a serverless function containing files and a `Makefile` to build
the filesystem for the function.
