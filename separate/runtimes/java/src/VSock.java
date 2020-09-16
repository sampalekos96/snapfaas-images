
package com.sns;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class VSock {

    private int fd;
    private native int vsock_connect(int cid, int port);
    private native String vsock_read(int fd);
    private native void vsock_write(int fd, String payload);
    private native void vscok_close(int fd);

    public VSock(int cid, int port) throws IOException {
        this.fd = this.vsock_connect(cid, port);
        if (this.fd < 0) {
            throw new IOException("vsock initialization exception");
        }
    }

    public void printVSock() {
        System.out.println("VSock support for Java");
    }

    static {
        System.loadLibrary("vsock");
    }

    public String vsockRead() throws IOException {
        String readStr = this.vsock_read(this.fd);
        if (null == readStr) {
            throw new IOException("vsock read exception");
        }
        return readStr;
    }

    public void vsockWrite(String utfString) {
        this.vsock_write(this.fd, utfString);
    }

    public void vsockClose() {
        this.vscok_close(this.fd);
    }

}
