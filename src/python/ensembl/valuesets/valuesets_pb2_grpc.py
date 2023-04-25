# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import valuesets_pb2 as valuesets__pb2


class ValueSetStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetValueSetByAccessionId = channel.unary_unary(
                '/ValueSet/GetValueSetByAccessionId',
                request_serializer=valuesets__pb2.ValueSetRequest.SerializeToString,
                response_deserializer=valuesets__pb2.ValueSetResponse.FromString,
                )
        self.GetValueSetsByValue = channel.unary_stream(
                '/ValueSet/GetValueSetsByValue',
                request_serializer=valuesets__pb2.ValueSetRequest.SerializeToString,
                response_deserializer=valuesets__pb2.ValueSetResponse.FromString,
                )
        self.GetValueSetsByDomain = channel.unary_stream(
                '/ValueSet/GetValueSetsByDomain',
                request_serializer=valuesets__pb2.ValueSetRequest.SerializeToString,
                response_deserializer=valuesets__pb2.ValueSetResponse.FromString,
                )
        self.GetValueSetStream = channel.unary_stream(
                '/ValueSet/GetValueSetStream',
                request_serializer=valuesets__pb2.ValueSetRequest.SerializeToString,
                response_deserializer=valuesets__pb2.ValueSetResponse.FromString,
                )


class ValueSetServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetValueSetByAccessionId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetValueSetsByValue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetValueSetsByDomain(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetValueSetStream(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ValueSetServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetValueSetByAccessionId': grpc.unary_unary_rpc_method_handler(
                    servicer.GetValueSetByAccessionId,
                    request_deserializer=valuesets__pb2.ValueSetRequest.FromString,
                    response_serializer=valuesets__pb2.ValueSetResponse.SerializeToString,
            ),
            'GetValueSetsByValue': grpc.unary_stream_rpc_method_handler(
                    servicer.GetValueSetsByValue,
                    request_deserializer=valuesets__pb2.ValueSetRequest.FromString,
                    response_serializer=valuesets__pb2.ValueSetResponse.SerializeToString,
            ),
            'GetValueSetsByDomain': grpc.unary_stream_rpc_method_handler(
                    servicer.GetValueSetsByDomain,
                    request_deserializer=valuesets__pb2.ValueSetRequest.FromString,
                    response_serializer=valuesets__pb2.ValueSetResponse.SerializeToString,
            ),
            'GetValueSetStream': grpc.unary_stream_rpc_method_handler(
                    servicer.GetValueSetStream,
                    request_deserializer=valuesets__pb2.ValueSetRequest.FromString,
                    response_serializer=valuesets__pb2.ValueSetResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ValueSet', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ValueSet(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetValueSetByAccessionId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ValueSet/GetValueSetByAccessionId',
            valuesets__pb2.ValueSetRequest.SerializeToString,
            valuesets__pb2.ValueSetResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetValueSetsByValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/ValueSet/GetValueSetsByValue',
            valuesets__pb2.ValueSetRequest.SerializeToString,
            valuesets__pb2.ValueSetResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetValueSetsByDomain(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/ValueSet/GetValueSetsByDomain',
            valuesets__pb2.ValueSetRequest.SerializeToString,
            valuesets__pb2.ValueSetResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetValueSetStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/ValueSet/GetValueSetStream',
            valuesets__pb2.ValueSetRequest.SerializeToString,
            valuesets__pb2.ValueSetResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
