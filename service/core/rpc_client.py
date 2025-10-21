"""gRPC client for communicating with Spark API service."""

import os
import sys
from collections.abc import Iterator
from typing import Any

import grpc

# Add lib directory to path for proto imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../lib'))

import sparkapi_pb2
import sparkapi_pb2_grpc
from exceptions import ApplicationError


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
            request = sparkapi_pb2.NewSessionRequest(session_id=request_data.get('session_id', ''), name=request_data.get('name', ''))
            response = self.client.createSession(request)
            return {'session_id': response.session_id, 'msg': response.msg}
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code='500') from e

    def get_session_status(self, session_id: str) -> dict[str, Any]:
        """Get session status."""
        try:
            request = sparkapi_pb2.SessionStatusRequest(session_id=session_id)
            response = self.client.getSessionStatus(request)
            return {'session_id': response.session_id, 'rebuild_recommendation': response.rebuild_recommendation, 'cause': response.cause}
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code='500') from e

    # TRANSFORM METHODS
    def submit_load_dataset_node(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Submit load dataset node."""
        try:
            # Create the appropriate input metadata based on the request
            request_args = {'session_id': request_data.get('session_id', '')}

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

            request = sparkapi_pb2.LoadDatasetNodeRequest(**request_args)
            response = self.client.submit_LoadDatasetNode(request)
            return {'session_id': response.session_id, 'msg': response.msg, 'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns]}
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code='500') from e

    def submit_load_from_session_node(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Submit load from session node."""
        try:
            request = sparkapi_pb2.LoadFromSessionNodeRequest(
                session_id=request_data.get('session_id', ''), input_session_id=request_data.get('input_session_id', '')
            )
            response = self.client.submit_LoadFromSessionNode(request)
            return {'session_id': response.session_id, 'msg': response.msg, 'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns]}
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code='500') from e

    def submit_filter_node(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Submit filter node."""
        try:
            request = sparkapi_pb2.FilterNodeRequest(
                session_id=request_data.get('session_id', ''),
                node_id=request_data.get('node_id', ''),
                prev_node_id=request_data.get('prev_node_id', ''),
                expressions=request_data.get('expressions', []),
                matching=request_data.get('matching', ''),
            )
            response = self.client.submit_FilterNode(request)
            return {'session_id': response.session_id, 'msg': response.msg, 'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns]}
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code='500') from e

    def submit_new_column_node(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Submit new column node."""
        try:
            expressions = []
            for expr in request_data.get('expressions', []):
                expressions.append(sparkapi_pb2.AddColumnExpression(expression=expr.get('expression', ''), new_column_name=expr.get('col_name', '')))

            request = sparkapi_pb2.AddColumnNodeRequest(
                session_id=request_data.get('session_id', ''),
                node_id=request_data.get('node_id', ''),
                prev_node_id=request_data.get('prev_node_id', ''),
                user_input=expressions,
            )
            response = self.client.submit_AddColumnNode(request)
            return {'session_id': response.session_id, 'msg': response.msg, 'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns]}
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code='500') from e

    def submit_join_node(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Submit join node."""
        try:
            # Create join parameters
            join_params = sparkapi_pb2.JoinParams(
                join_relation=request_data.get('joinParams', {}).get('join_relation', ''),
                columns_to_keep=request_data.get('joinParams', {}).get('columns_to_keep', []),
                columns_to_add=request_data.get('joinParams', {}).get('columns_to_add', []),
                prefix_for_added_columns=request_data.get('joinParams', {}).get('prefix_for_added_columns', ''),
                join_criteria=request_data.get('joinParams', {}).get('join_criteria', []),
                criteria_matching=request_data.get('joinParams', {}).get('criteria_matching', ''),
            )

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
            return {'session_id': response.session_id, 'msg': response.msg, 'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns]}
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code='500') from e

    def submit_table_node(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Submit table node."""
        try:
            request = sparkapi_pb2.AddTableNodeRequest(
                session_id=request_data.get('session_id', ''), node_id=request_data.get('node_id', ''), prev_node_id=request_data.get('prev_node_id', '')
            )
            response = self.client.submit_TableNode(request)
            return {'session_id': response.session_id, 'msg': response.msg, 'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns]}
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code='500') from e

    def submit_histogram_node(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Submit histogram node."""
        try:
            request = sparkapi_pb2.AddHistogramNodeRequest(
                session_id=request_data.get('session_id', ''),
                node_id=request_data.get('node_id', ''),
                prev_node_id=request_data.get('prev_node_id', ''),
                y_axis_col=request_data.get('y_axis_col', ''),
                order_by=request_data.get('order_by', ''),
                sort_by=request_data.get('sort_by', ''),
                expression=request_data.get('expression', ''),
            )
            response = self.client.submit_HistogramNode(request)
            return {'session_id': response.session_id, 'msg': response.msg, 'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns]}
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code='500') from e

    def remove_node(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Remove a node."""
        try:
            request = sparkapi_pb2.NodeRemovalRequest(session_id=request_data.get('session_id', ''), node_id=request_data.get('node_id', ''))
            response = self.client.removeNode(request)
            return {'session_id': response.session_id, 'msg': response.msg, 'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns]}
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code='500') from e

    # ACTION METHODS
    def preview_dataset(self, request_data: dict[str, Any]) -> Iterator[str]:
        """Preview dataset with streaming response."""
        try:
            request = sparkapi_pb2.PreviewDatasetRequest(
                session_id=request_data.get('session_id', ''), node_id=request_data.get('node_id', ''), limit=request_data.get('limit', 100)
            )

            for response in self.client.previewDataset(request):
                yield response.data

        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code='500') from e

    def summarize_dataset(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Summarize dataset."""
        try:
            request = sparkapi_pb2.SummarizeDatasetRequest(session_id=request_data.get('session_id', ''), node_id=request_data.get('node_id', ''))
            response = self.client.summarizeDataset(request)
            return {'session_id': response.session_id, 'msg': response.msg, 'columns': response.columns, 'schema': response.schema, 'count': response.count}
        except grpc.RpcError as e:
            raise ApplicationError(message=str(e), code='500') from e
