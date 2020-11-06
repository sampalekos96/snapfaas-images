
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <linux/vm_sockets.h>
#include "edu_princeton_sns_VSock.h"


JNIEXPORT jint JNICALL Java_edu_princeton_sns_VSock_vsock_1connect
  (JNIEnv *env, jobject thisObj, jint cid, jint port) {

    int fd;
    struct sockaddr_vm sa = {
        .svm_family =  AF_VSOCK,
    };
    sa.svm_cid = cid;
    sa.svm_port = port;

    fd = socket(AF_VSOCK, SOCK_STREAM, 0);
    if (fd < 0) {
    	perror("Err in creating socket");
    	return fd;
    }

    if (connect(fd, (struct sockaddr*)&sa, sizeof(sa)) != 0) {
    	perror("Err in connecting to host");
    	close(fd);
    	return -1;
    }

    return fd;
}

#define LEN_HEADER 4
JNIEXPORT jstring JNICALL Java_edu_princeton_sns_VSock_vsock_1read
  (JNIEnv *env, jobject thisObj, jint fd) {

    char *recv_str = NULL;
    unsigned char header[LEN_HEADER];

    int status = read(fd, header, LEN_HEADER);
    if (status < 0) {
        perror("Err in socket header reading");
        return NULL;
    }
    int len = (unsigned int)header[3] | (unsigned int)header[2]<<8 
            | (unsigned int)header[1]<<16 | (unsigned int)header[0]<<24;

    recv_str = (char*)malloc(len+1);
    if (NULL == recv_str) {
        perror("Err in malloc");
        return NULL;
    }

    status = read(fd, recv_str, len);
    if (status != len) {
    	perror("Err in socket reading");
    	return NULL;
    }
    recv_str[len] = '\0';

    jstring return_str = (*env)->NewStringUTF(env, recv_str);
    free(recv_str);
    return return_str;
}

JNIEXPORT void JNICALL Java_edu_princeton_sns_VSock_vsock_1write
  (JNIEnv *env, jobject thisObj, jint fd, jstring jsend) {

	const char *csend = (*env)->GetStringUTFChars(env, jsend, NULL);
	if (NULL == csend) {
		perror("Err in converting strings");
		return;
	}

	int len_str = strlen(csend);
	int mask = 0xFF;
	char header[LEN_HEADER];

	for (int i=0; i<LEN_HEADER; i++) {
		header[LEN_HEADER-1-i] = (len_str>>(i*8)) & mask;
	}

	int status = write(fd, header, LEN_HEADER);
	if (status != LEN_HEADER) {
		perror("Err in socket header writing");
		return;
	}
	status = write(fd, csend, len_str);
	if (status != len_str) {
		perror("Err in socket body writing");
		return;
	}

	return;
}

JNIEXPORT void JNICALL Java_edu_princeton_sns_VSock_vscok_1close
  (JNIEnv *env, jobject thisObj, jint fd) {

  	close(fd);
  	return;
}
