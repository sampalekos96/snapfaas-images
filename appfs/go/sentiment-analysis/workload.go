package main

import (
	"encoding/json"
	"fmt"

	"github.com/cdipaolo/sentiment"
)

var model sentiment.Models

func Init() {
	var err error
	model, err = sentiment.Restore()
	if err != nil {
		panic(fmt.Sprintf("Could not restore model!\n\t%v\n", err))
	}
}

type Response struct {
	Analysis *sentiment.Analysis
	Error    error
}

func Handle(reqBytes []byte) interface{} {
	type Request struct {
		Analyse string `json:analyse`
	}

	request := new(Request)
	err := json.Unmarshal(reqBytes, request)
	if err != nil {
		return &Response{
			Analysis: nil,
			Error:    err,
		}
	}

	resp := Response{
		Analysis: model.SentimentAnalysis(request.Analyse, sentiment.English),
		Error:    nil,
	}

	return resp
}
