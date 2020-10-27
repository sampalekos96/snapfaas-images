#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <linux/vm_sockets.h>

static int vsock_connect(int cid, int port)
{
	int fd;
	struct sockaddr_vm sa = {
    .svm_family =  AF_VSOCK,
  };
	sa.svm_cid = cid;
	sa.svm_port = port;

	fd = socket(AF_VSOCK, SOCK_STREAM, 0);
	if (fd < 0) {
		perror("socket");
		return -1;
	}

	if (connect(fd, (struct sockaddr*)&sa, sizeof(sa)) != 0) {
		perror("connect");
		close(fd);
		return -1;
	}

	return fd;
}

char *payload = "{\"body\": \"hello, world!\"}";

int main() {
  char throwaway[1];
  write(4, throwaway, 1);
  close(4); // Ready for a snapshot!

  read(3, throwaway, 1); // Wait for snapshot to be done
  close(3);

  int vsock = vsock_connect(2, 1234);
  if (vsock < 0) {
    exit(-1);
  }

  for (;;) {
    uint32_t buffer_length = 0;
    read(vsock, (char*)&buffer_length, 4);
    buffer_length = ntohl(buffer_length);
    char *buffer = (char*)malloc(buffer_length);
    read(vsock, buffer, buffer_length);

    free(buffer);

    uint32_t payload_len = strlen(payload);
    uint32_t payload_len_buf = htonl(payload_len);
    write(vsock, (char*)&payload_len_buf, 4);
    write(vsock, payload, payload_len);
  }
}
