#define _GNU_SOURCE

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include <dlfcn.h>
#include <fcntl.h>
#include <sched.h>
#include <unistd.h>

#include <arpa/inet.h>

#include <sys/io.h>
#include <sys/ioctl.h>
#include <sys/mount.h>

#include <linux/random.h>
#include <linux/vm_sockets.h>

typedef void initfunc(void);
typedef void responder(char*, uint32_t);
typedef void handlefunc(char*,uint32_t,responder);

#ifdef TEST
static int vsock_connect(int cid, int port)
{
  return 0;
}
#else
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
#endif

#ifdef TEST
// Fake snapshot function for local testing
void snapshot() {
  setbuf(stdout, NULL);
  printf("Snapshotting...");
  for (int i = 0; i < 100000000; i++) {
    asm("nop");
  }
  printf("Done\n");
}
#else
void snapshot() {
  // Make sure we are allowed to perform `outl`
  if (iopl(3)) {perror("iopl"); exit(1);}

  cpu_set_t cset;
  // Let VMM know each of the CPUS is ready for a snapshot
  for (int cpu = 1; ; cpu++) {
    CPU_ZERO(&cset);
    CPU_SET(cpu, &cset);
    if (sched_setaffinity(0, sizeof(cpu_set_t), &cset) < 0) {
      // If we got an error assume it's because the CPU doesn't exist, so we're done
      break;
    } else {
      outl(124, 0x3f0);
    }
  }

  // Finally, signal the VMM to start snapshotting from the main CPU
  CPU_ZERO(&cset);
  CPU_SET(0, &cset);
  sched_setaffinity(0, sizeof(cset), &cset);
  outl(124, 0x3f0);
}
#endif

int vsock;

static void respond(char *response, uint32_t response_len) {
  uint32_t response_len_buf = htonl(response_len);
  write(vsock, (char*)&response_len_buf, 4);
  write(vsock, response, response_len);
}

int main(int argc, char* argv[]) {
  snapshot();

#ifndef TEST
  // Mount the function filesystem
  if (mount("/dev/vdb", "/srv", "ext2", MS_RDONLY, NULL) < 0) {
    perror("mount");
  }
#endif

  void *libhandle = dlopen(argv[1], RTLD_NOW);
  initfunc *init = dlsym(libhandle, "init");
  handlefunc *handle = dlsym(libhandle, "handle");

  init();

  snapshot();

  vsock = vsock_connect(2, 1234);
  if (vsock < 0) {
    exit(-1);
  }
  printf("connected\n");

  for (;;) {
    uint32_t buffer_length = 0;
    read(vsock, (char*)&buffer_length, 4);
    buffer_length = ntohl(buffer_length);
    char *buffer = (char*)malloc(buffer_length);
    read(vsock, buffer, buffer_length);

    handle(buffer, buffer_length, &respond);
  }
}

