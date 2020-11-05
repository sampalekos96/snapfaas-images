apk add bash openjdk8 build-base make linux-headers maven

export JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk

# Copy application over
cp -r /my-app/* /srv

cd /runtime ; mvn clean package ; cd /
cp /runtime/vsock-native/target/*.so /lib/
cp /runtime/runtime/target/*dependencies.jar /bin/RuntimeWorkload.jar

cp /runtime/workload.sh /bin/runtime-workload
chmod +x /bin/runtime-workload

apk del build-base make linux-headers maven
