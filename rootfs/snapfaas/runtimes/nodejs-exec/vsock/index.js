const fs = require('fs');

const bindings = require('bindings')('vsock');

exports.connect = bindings.connect;
exports.read = bindings.read;

exports.readRequest = function(fd) {
  let len = 0;
  let lenBuf = Buffer.alloc(4);
  bindings.read(fd, lenBuf);
  len = lenBuf.readUInt32BE();
  let requestBuf = Buffer.alloc(len);
  bindings.read(fd, requestBuf);
  return JSON.parse(requestBuf);
}

exports.writeResponse = function(fd, resp) {
  let respBuf = JSON.stringify(resp);
  let buf = Buffer.alloc(4 + respBuf.length);
  let offset = buf.writeUInt32BE(respBuf.length);
  buf.write(respBuf, offset);
  fs.writeSync(fd, buf);
}

