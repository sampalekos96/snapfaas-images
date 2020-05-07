Directory `combined` contains code and scripts to generate root file systems each of which contain
**both** a language runtime and an application.

Directory `separate` contains code and scripts to generate root file systems each of which contain
just one language runtime. The root file system contains a wrapper of the langauge that expects a
second file system which contains an application.

Directory `appfs` contains applications each of which is a subdirectory.
