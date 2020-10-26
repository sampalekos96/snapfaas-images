apk add bash openjdk8 build-base make linux-headers

export JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk
export PATH="$JAVA_HOME/bin:${PATH}"

cp /runtime/lib/*.jar /lib/

javac -h /runtime/src/ -d /tmp/ /runtime/src/edu/princeton/sns/VSock.java
gcc -fPIC -I"${JAVA_HOME}/include" -I"${JAVA_HOME}/include/linux" -shared -o /lib/libvsock.so /runtime/src/vsock.c
jar -cvf /lib/VSock.jar -C /tmp edu

ls /lib/*.jar
ls /lib/*.so
javac -cp ".:/lib/json-simple-1.1.1.jar:/lib/VSock.jar" -d /bin/ /runtime/src/RuntimeWorkload.java
ls /bin/RuntimeWorkload.class

cp /runtime/workload.sh /bin/runtime-workload
chmod +x /bin/runtime-workload

apk del build-base make linux-headers
