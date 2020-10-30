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

int main() {
  // Pretend random number generator has been properly seeded
  int rand = open("/dev/random", 0);
  int amount = 10241024;
  if (ioctl(rand, RNDADDTOENTCNT, &amount) < 0) {
    perror("ioctl");
  }

  // Make sure we are allowed to perform `outl`
  if (iopl(3)) {perror("iopl"); exit(1);}

  // Let VMM know each of the CPUS is ready for a snapshot
  cpu_set_t *cset = CPU_ALLOC(8); // assumes we'll never have more than 8 CPUs
  for (int cpu = 1; ; cpu++) {
    CPU_ZERO(cset);
    CPU_SET(cpu, cset);
    if (sched_setaffinity(0, sizeof(cpu_set_t), cset) < 0) {
      // If we got an error assume it's because the CPU doesn't exist, so we're done
      break;
    } else {
      outl(124, 0x3f0);
    }
  }

  // Finally, signal the VMM to start snapshotting from the main CPU
  CPU_ZERO(cset);
  CPU_SET(0, cset);
  sched_setaffinity(0, sizeof(cpu_set_t), cset);
  outl(124, 0x3f0);

  // Mount the function filesystem
  //mount("/dev/vdb", "/srv", "ext4", 0, "ro");

  // let us fork then exec which is what Python's subprocess.call do
  char * args[] = {"outl", "126", "0x3f0", NULL};
  pid_t pid;
  if(pid = fork()) {
      // parent
      waitpid(pid, NULL, 0);
  } else {
      // child
      // OK, VMM, we're ready for requests
      execv("/usr/bin/outl", args);
  }
}

