apk add bash openjdk8

cp /runtime/lib/*.jar /bin/
cp /runtime/lib/*.so /bin/

cp /runtime/*.class /bin/
cp /runtime/workload.sh /bin/runtime-workload
chmod +x /bin/runtime-workload
