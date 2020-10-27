#define _GNU_SOURCE

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include <fcntl.h>
#include <sched.h>
#include <unistd.h>

#include <sys/io.h>
#include <sys/ioctl.h>
#include <sys/mount.h>
#include <sys/wait.h>

#include <linux/random.h>

#ifndef FAKE_SNAP
void snapshot() {
  // Make sure we are allowed to perform `outl`
  if (iopl(3)) {perror("iopl"); exit(1);}

  // Let VMM know each of the CPUS is ready for a snapshot
  for (int cpu = 1; ; cpu++) {
    cpu_set_t cset;
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
  cpu_set_t cset;
  CPU_ZERO(&cset);
  CPU_SET(0, &cset);
  sched_setaffinity(0, sizeof(cset), &cset);
  outl(124, 0x3f0);
}
#else
// Fake snapshot function for local testing
void snapshot() {
  setbuf(stdout, NULL);
  printf("Snapshotting...");
  for (int i = 0; i < 100000000; i++) {
    asm("nop");
  }
  printf("Done\n");
}
#endif

int main(int argc, char* argv[]) {
  snapshot();

  // Mount the function filesystem
  if (mount("/dev/vdb", "/srv", "ext2", MS_RDONLY, NULL) < 0) {
    perror("mount");
  }

  // We'll signal readiness between parent & child using a pipe.
  int p2c_pipefds[2];
  pipe(p2c_pipefds);
  int c2p_pipefds[2];
  pipe(c2p_pipefds);

  int pid = fork();
  if (pid == 0) {
    // Child process

    // Close parent's side of pipes
    close(p2c_pipefds[1]);
    close(c2p_pipefds[0]);

    dup2(p2c_pipefds[0], 3); // read from parent
    dup2(c2p_pipefds[1], 4); // write to parent
    // Run, child!
    char *argv2[2] = { argv[1], NULL };
    exit(execv(argv[1], argv2));
  } else {
    // Parent process

    // Close child's side of pipes
    close(p2c_pipefds[0]);
    close(c2p_pipefds[1]);

    // Wait for child pipe to close;
    char throwaway[1];
    read(c2p_pipefds[0], throwaway, 1);
    close(c2p_pipefds[0]);

    snapshot();

    // Signal child we're done snapshotting and it can open vsock
    write(p2c_pipefds[1], throwaway, 1);
    close(p2c_pipefds[1]);

    // Wait for the child to exit
    int status;
    do {
      waitpid(pid, &status, 0);
    } while (!WIFEXITED(status));
    exit(WEXITSTATUS(status));
  }
}

