const vsock = require("vsock");
const { execSync, exec } = require("child_process");

// for snapshot
// this approach relies on that we are currently being executed on cpu 0
// and that other cpus writes to the port before us
// since as of now snapshots are created offline, we are fine
const cpu_count = require("os").cpus().length;
for (var i = 1; i < cpu_count; i++) {
    exec(`taskset -c ${i} outl 124 0x3f0`);
}
execSync('taskset -c 0 outl 124 0x3f0')

execSync("mount -r /dev/vdb /srv");

module.paths.push("/srv/node_modules");
const app = require("/srv/workload");

for (var i = 1; i < cpu_count; i++) {
    exec(`taskset -c ${i} outl 124 0x3f0`);
}
execSync('taskset -c 0 outl 124 0x3f0')

const sock_conn = vsock.connect(2, 1234);

(async function() {
  execSync('taskset -c 0 outl 124 0x3f0')
  while (true) {
    const req = await vsock.readRequest(sock_conn);

    const hrstart = process.hrtime();
    const resp = await app.handle(req);
    const hrend = process.hrtime(hrstart)
    resp.duration = hrend[0] * 1000000000 + hrend[1];
    await vsock.writeResponse(sock_conn, resp);
  }
})();

