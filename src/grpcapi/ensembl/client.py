#  See the NOTICE file distributed with this work for additional information
#  regarding copyright ownership.
#
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""Ensembl ValueSets client example."""

import grpc
from grpcapi.ensembl.valuesets.valuesets_pb2 import ValueSetRequest
from grpcapi.ensembl.valuesets.valuesets_pb2_grpc import ValueSetStub

from typer import Typer

client_app = Typer()


def init_client():
    channel = grpc.insecure_channel("localhost:50051")
    return ValueSetStub(channel)


@client_app.command()
def get_ok():
    client = init_client()
    request = ValueSetRequest(accession_id="mane.select.1")
    print(client.GetValueSetByAccessionId(request))


@client_app.command()
def get_ko():
    client = init_client()
    request = ValueSetRequest(accession_id="foobar")
    print(client.GetValueSetByAccessionId(request))


@client_app.command()
def get_vs_by_accession(accession_id: str):
    client = init_client()
    request = ValueSetRequest(accession_id=accession_id)
    print(client.GetValueSetByAccessionId(request))


@client_app.command()
def get_vs_by_topic(topic: str, noncurrent: bool = False):
    client = init_client()
    request = ValueSetRequest(accession_id=topic, use_noncurrent=noncurrent)
    for vv in client.GetValueSetsByTopic(request):
        is_curr = "Current" if vv.is_current else "Not current"
        print(f"{vv.accession_id} - {is_curr}")


if __name__ == "__main__":
    client_app()
