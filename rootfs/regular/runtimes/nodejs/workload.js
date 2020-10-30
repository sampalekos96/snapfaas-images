const vsock = require("vsock");
const { execSync, exec } = require("child_process");

module.paths.push("/srv/node_modules");
const app = require("/srv/workload");

const sock_conn = vsock.connect(2, 1234);

(async function() {
  while (true) {
    const req = await vsock.readRequest(sock_conn);

    const hrstart = process.hrtime();
    const resp = await app.handle(req);
    const hrend = process.hrtime(hrstart)
    resp.runtime_sec = hrend[0];
    resp.runtime_ms = hrend[1] / 1000000;
    await vsock.writeResponse(sock_conn, resp);
  }
})();

