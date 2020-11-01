package main

import (
	"fmt"
)

func Init() {
	fmt.Printf("Initializing\n")
}

type Response struct {
}

func Handle([]byte) interface{} {
	return Response{}
}
