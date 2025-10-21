from collections.abc import Iterator
import re
from typing import Any

import grpc
import sparkapi_pb2
import sparkapi_pb2_grpc

from .exceptions import ApplicationError


class RpcClient:
    """Singleton gRPC client for Spark API communication."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # Create gRPC channel and stub
        self.channel = grpc.insecure_channel('localhost:50051')
        self.client = sparkapi_pb2_grpc.SparkApiStub(self.channel)
        self._initialized = True

    def __del__(self):
        if hasattr(self, 'channel'):
            self.channel.close()

    # SESSION METHODS
    def create_session(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Create a new Spark session."""
        try:
            request = sparkapi_pb2.NewSessionRequest(**request_data)
            response = self.client.createSession(request)
            return response
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code=500) from e

    def load_sessions(self) -> Iterator[dict[str, Any]]:
        """Load all sessions with streaming response."""
        try:
            request = sparkapi_pb2.Empty()
            for response in self.client.loadSessions(request):
                yield {
                    'session_id': response.session_id,
                    'name': response.name,
                    'nodes': response.nodes,
                }
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code=500) from e

    def get_session_status(self, session_id: str) -> dict[str, Any]:
        """Get session status."""
        try:
            request = sparkapi_pb2.SessionStatusRequest(session_id=session_id)
            response = self.client.getSessionStatus(request)
            return {'session_id': response.session_id, 'status': response.status}
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code=500) from e

    # TRANSFORM METHODS
    def submit_load_dataset_node(self, request_data: dict[str, Any]) -> Iterator[dict[str, Any]]:
        """Submit load dataset node with streaming response."""
        try:
            print('RPC Client - submit_load_dataset_node called with:', request_data)
            request = sparkapi_pb2.LoadDatasetNodeRequest(
                session_id=request_data.get('session_id', ''), parquet=sparkapi_pb2.ParquetInput(**request_data.get('parquet', {}))
            )
            # For streaming responses, iterate over the response stream
            for response in self.client.submit_LoadDatasetNode(request):
                print('RPC Client - submit_load_dataset_node received response:', response)
                try:
                    yield response
                except Exception as e:
                    print('RPC Client - submit_load_dataset_node error:', e)
                    # yield {'error': str(e)}
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code=500) from e

    def submit_load_from_session_node(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Submit load from session node."""
        try:
            request = sparkapi_pb2.LoadFromSessionNodeRequest(**request_data)
            response = self.client.submit_LoadFromSessionNode(request)
            return response
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code=500) from e

    def submit_filter_node(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Submit filter node."""
        try:
            request = sparkapi_pb2.FilterNodeRequest(**request_data)
            response = self.client.submit_FilterNode(request)
            return response
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code=500) from e

    def submit_new_column_node(self, request_data: dict[str, Any]) -> Iterator[dict[str, Any]]:
        """Submit new column node with streaming response."""
        try:
            expressions = []
            for expr in request_data.get('expressions', []):
                expressions.append(sparkapi_pb2.AddColumnExpression(**expr))
            request = sparkapi_pb2.AddColumnNodeRequest(**request_data, user_input=expressions)
            yield from self.client.submit_AddColumnNode(request)
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code=500) from e

    def submit_join_node(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Submit join node."""
        try:
            # Create join parameters
            join_params = sparkapi_pb2.JoinParams(**request_data.get('joinParams', {}))

            request_args = {
                'session_id': request_data.get('session_id', ''),
                'node_id': request_data.get('node_id', ''),
                'prev_node_id': request_data.get('prev_node_id', ''),
                'joinParams': join_params,
            }

            # Add input metadata
            if 'csv' in request_data:
                csv_input = sparkapi_pb2.CsvInput(
                    delimiter=request_data['csv'].get('delimiter', ','),
                    include_header=request_data['csv'].get('include_header', True),
                    path=request_data['csv'].get('path', ''),
                )
                request_args['csv'] = csv_input
            elif 'json' in request_data:
                json_input = sparkapi_pb2.JsonInput(multiline=request_data['json'].get('multiline', False), path=request_data['json'].get('path', ''))
                request_args['json'] = json_input
            elif 'parquet' in request_data:
                parquet_input = sparkapi_pb2.ParquetInput(path=request_data['parquet'].get('path', ''))
                request_args['parquet'] = parquet_input
            elif 'session' in request_data:
                session_input = sparkapi_pb2.SessionInput(session_id=request_data['session'].get('session_id', ''))
                request_args['session'] = session_input

            request = sparkapi_pb2.JoinNodeRequest(**request_args)
            response = self.client.submit_JoinNode(request)
            return response
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code=500) from e

    def submit_table_node(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Submit table node."""
        try:
            request = sparkapi_pb2.AddTableNodeRequest(**request_data)
            response = self.client.submit_TableNode(request)
            return response
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code=500) from e

    def submit_histogram_node(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Submit histogram node."""
        try:
            request = sparkapi_pb2.AddHistogramNodeRequest(**request_data)
            response = self.client.submit_HistogramNode(request)
            return response
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code=500) from e

    def remove_node(self, request_data: dict[str, Any]) -> Iterator[dict[str, Any]]:
        """Remove a node with streaming response."""
        try:
            request = sparkapi_pb2.NodeRemovalRequest(**request_data)
            yield from self.client.removeNode(request)
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code=500) from e

    def toggle_node(self, request_data: dict[str, Any]) -> Iterator[dict[str, Any]]:
        """Toggle a node with streaming response."""
        try:
            request = sparkapi_pb2.NodeToggleRequest(**request_data)
            yield from self.client.toggleNode(request)
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code=500) from e

    # ACTION METHODS
    def preview_dataset(self, request_data: dict[str, Any]) -> Iterator[str]:
        """Preview dataset with streaming response."""
        try:
            print('RPC Client - preview_dataset called with:', request_data)
            request = sparkapi_pb2.PreviewDatasetRequest(**request_data)

            for response in self.client.previewDataset(request):
                yield response.data

        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code=500) from e

    def summarize_dataset(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Summarize dataset."""
        try:
            request = sparkapi_pb2.SummarizeDatasetRequest(**request_data)
            response = self.client.summarizeDataset(request)
            return response
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code=500) from e
