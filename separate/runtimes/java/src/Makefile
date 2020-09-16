
all: vsock java_classes
	mv *.class ../

vsock:
	javac -h . VSock.java
	gcc -fPIC -I"${JAVA_HOME}/include" -I"${JAVA_HOME}/include/linux" -shared -o libvsock.so vsock.c
	mkdir -p com/sns
	mv VSock.class com/sns/
	jar -cvf ../lib/VSock.jar com/*
	rm -rf com/
	mv libvsock.so ../lib/

java_classes:
	javac setup_java.java
	javac -cp ".:../lib/*" runtime_workload.java

