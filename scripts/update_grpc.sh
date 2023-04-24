#!/usr/bin/env bash

# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

REPO_ROOT=../
SRC_ROOT=../src/python/

python -m grpc_tools.protoc -I ${REPO_ROOT}/protobufs \
	--python_out=${SRC_ROOT}/ensembl/valuesets \
	--grpc_python_out=${SRC_ROOT}/ensembl/valuesets \
	${REPO_ROOT}/protobufs/valuesets.proto
