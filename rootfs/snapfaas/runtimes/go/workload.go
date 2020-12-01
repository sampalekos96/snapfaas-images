package main

import (
	"encoding/binary"
	"encoding/json"
	"os"
	"os/exec"
	"plugin"
	"runtime"

	"golang.org/x/sys/unix"
)

func main() {
	err := unix.Iopl(3)
	if err != nil {
		panic(err)
	}

	for i := 1; i < runtime.NumCPU(); i++ {
		exec.Command("taskset", "-c", string(i), "outl", "124", "0x3f0").Run()
	}
	exec.Command("taskset", "-c", "0", "outl", "124", "0x3f0").Run()

	if unix.Mount("/dev/vdb", "/srv", "ext2", unix.MS_RDONLY, "") != nil {
		panic("Failed to mount")
	}

	p, err := plugin.Open(os.Args[1])
	if err != nil {
		panic(err)
	}
	initptr, err := p.Lookup("Init")
	if err != nil {
		panic(err)
	}
	handleptr, err := p.Lookup("Handle")
	if err != nil {
		panic(err)
	}

	init := initptr.(func())
	handle := handleptr.(func([]byte) interface{})

	init()

	for i := 1; i < runtime.NumCPU(); i++ {
		exec.Command("taskset", "-c", string(i), "do-snapshot", "123").Run()
	}
	exec.Command("taskset", "-c", "0", "do-snapshot", "123").Run()

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

		response := handle(reqbuf)

		responseBuf, err := json.Marshal(response)

		binary.BigEndian.PutUint32(lenbuf, uint32(len(responseBuf)))
		_, err = unix.Write(fd, lenbuf)
		if err != nil {
			panic(err)
		}
		unix.Write(fd, responseBuf)
	}
}
