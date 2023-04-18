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


"""ValueSets RPC Server.

If executed as __main__ it will start a gRPC server, which allows to query EnsEMBL
ValueSets data.
ValueSet is defined according to the EnsEMBL Core Data Model (CDM)


"""

__all__ = [ ]

from concurrent import futures
import logging
import signal
import sys
#from typing import Generator
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from pathlib import Path
from urllib.parse import ParseResult, urlparse
import requests
import json

import grpc
from valuesets_pb2 import ValueSetResponse, ValueSetItem, CoreValueSetItem
from valuesets_pb2_grpc import ValueSetGetterServicer, add_ValueSetGetterServicer_to_server

vs_data_by_accession = {}

class ValueSetGetter(ValueSetGetterServicer):

    def GetValueSetByAccessionId(self, request, context: grpc.ServicerContext) -> ValueSetResponse:
        """Retrieves a ValueSet by its accession ID.

        Args:
            request (request): A string that is concatenated with "Hello "

        Returns:
            A string that is the result of the concatenation between "Hello " and `word`
        """
        logging.info("Serving GetValueSetByAccessionId request %s", request)
        req_acc_id = request.accession_id
        if req_acc_id not in vs_data_by_accession.keys():
            context.abort(grpc.StatusCode.NOT_FOUND, "Accession_id not found")
        (label, value, definition, description) = vs_data_by_accession[req_acc_id]
        vset = ValueSetItem(core_vset=CoreValueSetItem(accession_id=req_acc_id,
                                label=label,
                                value=value,
                                definition=definition,
                                description=description))
        return ValueSetResponse(valuesets=(vset,))


    def GetValueSetByValue(self, request, context: grpc.ServicerContext) -> ValueSetResponse:
        logging.info("Serving GetValueSetByValue request %s", request)
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "")
#        req_value = request.value
#        if value not in valuesets_data.values()[1]:
#            context.abort(grpc.StatusCode.NOT_FOUND, "Value not found")
#        (label, value, definition, description) = vs_data_by_value[acc_id]
#        vset = ValueSetItem(core_vset=CoreValueSetItem(accession_id=acc_id,
#                                label=label,
#                                value=value,
#                                definition=definition,
#                                description=description))
#        return ValueSetResponse(valuesets=(vset,))

    def GetValueSetStream(self, request, context: grpc.ServicerContext) -> Generator[ValueSetResponse, None, None]:
        logging.info("Serving GetValueSetStream request %s", request)
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "")


class GracefulKiller:
    def __init__(self, server):
        
        self._server = server
        signal.signal(signal.SIGINT, self.sigint_handler)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def sigint_handler(self, args*):
        logging.info("Received SIGINT. Shutting down ...")
        self.exit_gracefully()

    def sigterm_handler(self, args*):
        logging.info("Received SIGTERM. Shutting down ...")
        self.exit_gracefully()

    def exit_gracefully(self, *args):
        done = self._server.stop(None)
        done.wait(None)
        logging.info('Stop complete.')


def get_server(port: str):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ValueSetGetterServicer_to_server(ValueSetGetter(), server)
    listen_address = f'[::]:{port}'
    server.add_insecure_port(listen_address)
    logging.info("Starting server on %s", listen_address)
    return server


def load_vs_data_from_json(url: ParseResult):
    if url.scheme not in ('file', 'http', 'https'):
        logging.error('Invalid scheme for valuesets URL; must be "file", "http", "https"')
        raise ValueError(f'Invalid scheme for valuesets URL; must be "file", "http", "https"')

    global vs_data_by_accession
    if url.scheme == 'file':
        logging.info(f'Loading JSON from file URL: {url.geturl()}')
        filename = Path(url.netloc) / Path(url.path)
        if not filename.exists() or not filename.is_file():
            logging.error(f'Provided input filename {url} does not exists or is not a file')
            raise ValueError(f'Provided input filename {url} does not exists or is not a file')
        with open(filename, 'rt') as fh:
            vs_data_by_accession = json.load(fh)
    else:
        logging.info(f'Loading JSON from http(s) URL: {url.geturl()}')
        r = requests.get(url.geturl(), headers={ "Content-Type" : "application/json"})
        if not r.ok:
            logging.error(f'Request failed with code {r.status_code}')
            r.raise_for_status()
        vs_data_by_accession = r.json()


def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--port", default="50051", help="Server port")
    parser.add_argument("--valuesets-url", default="https://raw.githubusercontent.com/sgiorgetti/test-valuesets/main/valuesets.json", help="URL to valuesets JSON file")
    parser.add_argument("--log-level", default="INFO", help="Log level")
    args = vars(parser.parse_args())

    logging.basicConfig(
            stream=sys.stdout,
            format="%(asctime)s %(levelname)-8s %(name)-15s: %(message)s",
            level=args["log_level"],
            )

    load_vs_data_from_json(urlparse(args["valuesets_url"]))
    if not vs_data_by_accession:
        logging.error(f'Something went wrong with loading the ValueSets: cache is empty')
        raise Exception(f'Something went wrong with loading the ValueSets: cache is empty')

    server = get_server(args["port"])
    server.start()
    GracefulKiller(server)
    server.wait_for_termination()


if __name__ == '__main__':
    main()
