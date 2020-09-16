apk add bash openjdk8 build-base make linux-headers

export JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk
export PATH="$JAVA_HOME/bin:${PATH}"
make -C /runtime/src/

cp /runtime/lib/*.jar /bin/
cp /runtime/lib/*.so /bin/

cp /runtime/*.class /bin/
cp /runtime/workload.sh /bin/runtime-workload
chmod +x /bin/runtime-workload

apk del build-base make linux-headers
