package main

import (
	"fmt"

	"github.com/drhodes/golorem"
)

func Init() {
	fmt.Printf("Initializing\n")
}

type Response struct {
	Sentence string
}

func Handle([]byte) interface{} {
	return Response{
		Sentence: lorem.Sentence(10, 10),
	}
}
