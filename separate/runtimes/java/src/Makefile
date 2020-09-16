
all: vsock java_classes
	mv *.class ../

vsock:
	javac -h . VSock.java
	gcc -fPIC -I"${JAVA_HOME}/include" -I"${JAVA_HOME}/include/linux" -shared -o libvsock.so vsock.c
	mkdir -p edu/princeton/sns
	mv VSock.class edu/princeton/sns/
	jar -cvf ../lib/VSock.jar edu/*
	rm -rf edu/
	mv libvsock.so ../lib/

java_classes:
	javac -cp ".:../lib/*" runtime_workload.java

