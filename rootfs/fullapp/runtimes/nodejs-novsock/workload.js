const { execSync, exec } = require("child_process");
const cpu_count = require("os").cpus().length;

module.paths.push("/srv/node_modules");
const app = require("/srv/workload");

for (var i = 1; i < cpu_count; i++) {
    exec(`taskset -c ${i} outl 124 0x3f0`);
}
execSync('taskset -c 0 do-snapshot 126');

(async function() {
  while (true) {
    const hrstart = process.hrtime();
    const resp = await app.handle({});
    const hrend = process.hrtime(hrstart)
    resp.runtime_sec = hrend[0];
    resp.runtime_ms = hrend[1] / 1000000;
    for (var i = 1; i < cpu_count; i++) {
        exec(`taskset -c ${i} outl 124 0x3f0`);
    }
    execSync('taskset -c 0 outl 126 0x3f0');
  }
})();

