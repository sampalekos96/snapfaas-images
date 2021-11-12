import struct

def handle(obj, syscall):
    old = syscall.read_key(bytes("count", "utf-8"))
    count = 0
    if old:
        count = struct.unpack(">I", old)[0]
    syscall.write_key(bytes("count", "utf-8"), struct.pack(">I", count + 1))
    return {'count': count}
