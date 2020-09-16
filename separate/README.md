This folder holds the scripts to generate root file systems that contain only language runtime

Try `./mk_rtimage.sh` to see the usage.

To generate a Java root, please go to `runtimes/java/src/` and run `make` (make sure your environment variable `JAVA_HOME` points to your jdk directory, a typical path would look like `/usr/lib/jvm/java-8-openjdk-amd64`) first before calling `./mk_rtimage.sh`
