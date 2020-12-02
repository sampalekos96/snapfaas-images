package main

import (
	"encoding/binary"
	"encoding/json"
	"os/exec"
	"runtime"

	"golang.org/x/sys/unix"
)

func main() {
	Init()

	for i := 1; i < runtime.NumCPU(); i++ {
                exec.Command("taskset", "-c", string(i), "outl", "123", "0x3f0").Run()
        }
        exec.Command("taskset", "-c", "0", "outl", "123", "0x3f0").Run()

	fd, err := unix.Socket(unix.AF_VSOCK, unix.SOCK_STREAM, 0)
	if err != nil {
		panic(err)
	}
	sa := unix.SockaddrVM{
		CID:  2,
		Port: 1234,
	}
	err = unix.Connect(fd, &sa)
	if err != nil {
		panic(err)
	}

	for {
		lenbuf := make([]byte, 4)
		_, err = unix.Read(fd, lenbuf)
		if err != nil {
			panic(err)
		}
		reqlen := binary.BigEndian.Uint32(lenbuf)
		reqbuf := make([]byte, reqlen)
		_, err = unix.Read(fd, reqbuf)
		if err != nil {
			panic(err)
		}

		response := Handle(reqbuf)

		responseBuf, err := json.Marshal(response)

		binary.BigEndian.PutUint32(lenbuf, uint32(len(responseBuf)))
		_, err = unix.Write(fd, lenbuf)
		if err != nil {
			panic(err)
		}
		unix.Write(fd, responseBuf)
	}
}
