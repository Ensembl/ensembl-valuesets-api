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
import logging

import grpc
from valuesets_pb2 import (
        ValueSetList,
        ValueSetItem
)
from valuesets_pb2_grpc import(
        ValueSetServicer,
        add_ValueSetServicer_to_server
)
from ensembl.valuesets.config import Config, default_conf
from ensembl.valuesets.valuesets_data import *

__all__ = [ 'ValueSetGetterServicer', 'ValuesetsRPCServer' ]

_logger = logging.getLogger(__name__)

class ValueSetGetterServicer(ValueSetServicer):
    """Provides methods that implement functionality of ValueSets RPC server"""

    def __init__(self, vs_data) -> None:
        self._vs_data = vs_data
        super().__init__()

    def GetValueSetByAccessionId(
            self, request, context: grpc.ServicerContext
        ) -> ValueSetList:
        """Retrieves a ValueSet by its accession ID."""

        _logger.info("Serving GetValueSetByAccessionId '%s'", str(request.accession_id).rstrip())
        if not request.accession_id:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "accession_id invalid or None")

        data = self._vs_data.get_vsdata_by_accession_id(request.accession_id)
        
        if not data:
            return ValueSetList(valuesets=())
        
        vset = ValueSetItem(accession_id=data.accession_id,
                                label=data.label,
                                value=data.value,
                                is_current=data.is_current,
                                definition=data.definition,
                                description=data.description)
        return ValueSetList(valuesets=(vset,))


    def GetValueSetsByValue(
            self, request, context: grpc.ServicerContext
        ) -> ValueSetList:
        """Retrieves a list of ValueSet by their Value."""

        _logger.info("Serving GetValueSetsByValue '%s'", str(request.value).rstrip())
        if not request.value:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "value invalid or None")
        
        data = self._vs_data.get_vsdata_by_value(value=request.value, is_current=request.is_current)

        if not data:
            return ValueSetList(valuesets=())
        
        vset = (ValueSetItem(accession_id=datum.accession_id,
                            label=datum.label,
                            value=datum.value,
                            is_current=datum.is_current,
                            definition=datum.definition,
                            description=datum.description) for datum in data)
        return ValueSetList(valuesets=vset)


    def GetValueSetsByDomain(
            self, request, context: grpc.ServicerContext
        ) -> ValueSetList:
        """Retrieves a list of ValueSet by their Domain."""

        _logger.info("Serving GetValueSetsByDomain '%s'", str(request.accession_id).rstrip())
        if not request.accession_id:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "value invalid or None")
        
        data = self._vs_data.get_vsdata_by_domain(domain=request.accession_id, is_current=request.is_current)

        if not data:
            return ValueSetList(valuesets=())
        
        vset = (ValueSetItem(accession_id=datum.accession_id,
                            label=datum.label,
                            value=datum.value,
                            is_current=datum.is_current,
                            definition=datum.definition,
                            description=datum.description) for datum in data)
        return ValueSetList(valuesets=vset)
        

    def GetAllValueSets(
            self, request, context: grpc.ServicerContext
        ) -> Generator[ValueSetItem, None, None]:
        """Retrieves the entire ValueSet list"""

        curr_s = 'current ' if request.is_current else ''
        _logger.info("Serving GetValueSetStream for %sValuesets", curr_s)
        
        data = self._vs_data.get_all(request.is_current)

        if not data:
            return ValueSetItem()
        
        for datum in data:
            vset = ValueSetItem(accession_id=datum.accession_id,
                                label=datum.label,
                                value=datum.value,
                                is_current=datum.is_current,
                                definition=datum.definition,
                                description=datum.description)
            yield vset


class ValuesetsRPCServer():
    
    def __init__(self, config: Config = default_conf, vs_data: ValueSetData = None) -> None:
        if not isinstance(config, Config):
            raise ValueError("Invalid argument 'config'")
        if not isinstance(vs_data, ValueSetData) or not vs_data:
            raise ValueError("Invalid argument 'vs_data'")

        self._config: Config = config
        self._vs_data = vs_data
        self._server = None

        _logger.info(self._config)
    
    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}>({self._config})'

    def exit_gracefully(self):
        done = self._server.stop(self._config.stop_timeout)
        done.wait(self._config.stop_timeout)

    def serve(self):
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=self._config.max_workers))
        
        def sigint_handler(_signum, _frame):
            _logger.info("Received SIGINT. Shutting down ...")
            self.exit_gracefully()

        def sigterm_handler(_signum, _frame):
            _logger.info("Received SIGTERM. Shutting down ...")
            self.exit_gracefully()

        signal(SIGINT, sigint_handler)
        signal(SIGTERM, sigterm_handler)

        add_ValueSetServicer_to_server(ValueSetGetterServicer(self._vs_data), self._server)

        listen_address = f'[::]:{self._config.server_port}'
        self._server.add_insecure_port(listen_address)
        _logger.debug("Starting server on %s", listen_address)
        self._server.start()

        self._server.wait_for_termination()
        _logger.info('Stop complete.')


def main():
    config=default_conf
    logging.basicConfig(
            stream=sys.stdout,
            format="%(asctime)s %(levelname)-8s %(name)-15s: %(message)s",
            level=logging.DEBUG if config.debug else logging.INFO,
        )
    global _logger
    _logger = logging.getLogger('valuesets_rpc')
    vs_data = ValueSetData(config, autoload=True)
    srv = ValuesetsRPCServer(config, vs_data)
    srv.serve()


if __name__ == '__main__':
    main()
