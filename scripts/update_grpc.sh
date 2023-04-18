#!/usr/bin/env bash

SRC_ROOT=../src/ensembl/

python -m grpc_tools.protoc -I ${SRC_ROOT}/protobufs \
	--python_out=${SRC_ROOT}/valuesets \
	--grpc_python_out=${SRC_ROOT}/valuesets \
	${SRC_ROOT}/protobufs/valuesets.proto
