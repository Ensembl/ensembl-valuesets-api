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

# FROM python:3.8-slim
FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV SERVER_PORT 50051
ENV PYTHONPATH "/opt/ensembl-valuesets-api/src/python"

WORKDIR /opt

COPY . /opt/ensembl-valuesets-api/

WORKDIR /opt/ensembl-valuesets-api

RUN pip install --no-cache-dir .

CMD ["python", "src/python/ensembl/valuesets/valuesets_rpc_server.py"]
EXPOSE ${SERVER_PORT}
