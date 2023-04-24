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

from concurrent import futures
from signal import signal, SIGINT, SIGTERM
import sys
from typing import Generator

import grpc
from valuesets_pb2 import (
        ValueSetResponse,
        ValueSetItem,
        CoreValueSetItem
)
from valuesets_pb2_grpc import(
        ValueSetGetterServicer,
        add_ValueSetGetterServicer_to_server
)
from ensembl.valuesets.config import Config, default_conf
from ensembl.valuesets.valuesets_data import *

_logger = None
_config: Config = None
_vs_data = None

class ValueSetGetter(ValueSetGetterServicer):
    """Provides methods that implement functionality of ValueSets RPC server"""

    def GetValueSetByAccessionId(
            self, request, context: grpc.ServicerContext
        ) -> ValueSetResponse:
        """Retrieves a ValueSet by its accession ID."""

        _logger.info("Serving GetValueSetByAccessionId '%s'", str(request.accession_id).rstrip())
        if not request.accession_id:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "accession_id invalid or None")

        data = _vs_data.get_vsdata_by_accession_id(request.accession_id)
        vset = ValueSetItem(core_vset=CoreValueSetItem(accession_id=data.accession_id,
                                label=data.label,
                                value=data.value,
                                is_current=data.is_current,
                                definition=data.definition,
                                description=data.description))
        return ValueSetResponse(valuesets=(vset,))


    def GetValueSetsByValue(
            self, request, context: grpc.ServicerContext
        ) -> Generator[ValueSetResponse, None, None]:
        """Retrieves a list of ValueSet by their Value."""

        _logger.info("Serving GetValueSetsByValue '%s'", str(request.value).rstrip())
        if not request.value:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "value invalid or None")
        
        data = _vs_data.get_vsdata_by_value(value=request.value, is_current=request.is_current)
        
        vset = (ValueSetItem(core_vset=CoreValueSetItem(accession_id=datum.accession_id,
                            label=datum.label,
                            value=datum.value,
                            is_current=datum.is_current,
                            definition=datum.definition,
                            description=datum.description)) for datum in data)
        yield ValueSetResponse(valuesets=vset)


    def GetValueSetsByDomain(
            self, request, context: grpc.ServicerContext
        ) -> Generator[ValueSetResponse, None, None]:
        """Retrieves a list of ValueSet by their Domain."""

        _logger.info("Serving GetValueSetsByDomain '%s'", str(request.domain).rstrip())
        if not request.domain:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "value invalid or None")
        
        data = _vs_data.get_vsdata_by_domain(domain=request.domain, is_current=request.is_current)
        
        vset = (ValueSetItem(core_vset=CoreValueSetItem(accession_id=datum.accession_id,
                            label=datum.label,
                            value=datum.value,
                            is_current=datum.is_current,
                            definition=datum.definition,
                            description=datum.description)) for datum in data)
        yield ValueSetResponse(valuesets=vset)


    def GetValueSetStream(
            self, request, context: grpc.ServicerContext
        ) -> Generator[ValueSetResponse, None, None]:
        """Retrieves the entire ValueSet list"""

        curr_s = 'current ' if request.is_current else ''
        _logger.info("Serving GetValueSetStream for %sValuesets", curr_s)
        
        data = _vs_data.get_all(request.is_current)
        
        vset = (ValueSetItem(core_vset=CoreValueSetItem(accession_id=datum.accession_id,
                            label=datum.label,
                            value=datum.value,
                            is_current=datum.is_current,
                            definition=datum.definition,
                            description=datum.description)) for datum in data)
        yield ValueSetResponse(valuesets=vset)


def exit_gracefully(server):
    done = server.stop(_config.stop_timeout)
    done.wait(_config.stop_timeout)


def serve():
    _logger.info(_config)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=_config.max_workers))
    
    def sigint_handler(_signum, _frame):
        _logger.info("Received SIGINT. Shutting down ...")
        exit_gracefully()

    def sigterm_handler(_signum, _frame):
        _logger.info("Received SIGTERM. Shutting down ...")
        exit_gracefully()

    signal(SIGINT, sigint_handler)
    signal(SIGTERM, sigterm_handler)

    add_ValueSetGetterServicer_to_server(ValueSetGetter(), server)

    listen_address = f'[::]:{_config.server_port}'
    server.add_insecure_port(listen_address)
    _logger.debug("Starting server on %s", listen_address)
    server.start()

    server.wait_for_termination()
    _logger.info('Stop complete.')


def init_logger(logger=None):
    global _logger
    if logger is not None:
        _logger = logger
    else:
        import logging
        logging.basicConfig(
            stream=sys.stdout,
            format="%(asctime)s %(levelname)-8s %(name)-15s: %(message)s",
            level=logging.DEBUG if _config.debug else logging.INFO,
        )
        _logger = logging.getLogger('valuesets_rpc')


def init_config(config: Config):
    if not config:
        raise ValueError('Invalid argument "config"')
    global _config
    if _config and _config != config:
        raise Exception('Found existing config in module'
                        '"init_config" can be invoked only once.'
              )
    _config = config


def main(logger = None, config: Config = default_conf):
    init_config(config)
    init_logger(logger)
    global _vs_data
    global _config
    global _logger
    _vs_data = ValueSetData(_config, _logger, autoload=True)
    serve()


if __name__ == '__main__':
    main()
