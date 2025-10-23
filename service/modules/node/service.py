from collections.abc import Iterator
from typing import Any

import grpc
import sparkapi_pb2

from core.exceptions import ApplicationError
from core.rpc_client import RpcClient

rpc_client = RpcClient()


def preview_dataset(request_data: dict[str, Any]) -> Iterator[str]:
    """Preview dataset with streaming response."""
    try:
        request = sparkapi_pb2.PreviewDatasetRequest(**request_data)

        for response in rpc_client.client.previewDataset(request):
            response: sparkapi_pb2.DatasetResponse
            yield response.data

    except grpc.RpcError as e:
        raise ApplicationError(message=str(e), code=500) from e


def summarize_dataset(request_data: dict[str, Any]) -> dict[str, Any]:
    """Summarize dataset."""
    try:
        request = sparkapi_pb2.SummarizeDatasetRequest(**request_data)
        response: sparkapi_pb2.SparkActionResponse = rpc_client.client.summarizeDataset(request)
        return {
            'session_id': response.session_id,
            'msg': response.msg,
            'columns': response.columns,
            'schema': response.schema,
            'count': response.count,
        }
    except grpc.RpcError as e:
        raise ApplicationError(message=str(e), code=500) from e


def submit_load_dataset_node(request_data: dict[str, Any]) -> Iterator[dict[str, Any]]:
    """Submit load dataset node with streaming response."""
    try:
        request = sparkapi_pb2.LoadDatasetNodeRequest(
            session_id=request_data.get('session_id', ''),
            csv=sparkapi_pb2.CsvInput(**request_data['csv']) if request_data.get('csv') else None,
            json=sparkapi_pb2.JsonInput(**request_data['json']) if request_data.get('json') else None,
            parquet=sparkapi_pb2.ParquetInput(**request_data['parquet']) if request_data.get('parquet') else None,
        )

        for response in rpc_client.client.submit_LoadDatasetNode(request):
            response: sparkapi_pb2.SparkTransformResponse
            yield {
                'session_id': response.session_id,
                'node_id': response.node_id,
                'prev_node_id': response.prev_node_id,
                'invalid_state': {
                    'active': response.invalid_state.active,
                    'error_msg': response.invalid_state.error_msg,
                },
                'active': response.active,
                'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns],
                'title': response.title,
                'user_input': response.user_input,
            }

    except grpc.RpcError as e:
        raise ApplicationError(message=str(e), code=500) from e


def submit_add_column_node(request_data: dict[str, Any]) -> Iterator[dict[str, Any]]:
    """Submit add column node with streaming response."""
    try:
        request = sparkapi_pb2.AddColumnNodeRequest(
            session_id=request_data.get('session_id', ''),
            node_id=request_data.get('node_id', ''),
            prev_node_id=request_data.get('prev_node_id', ''),
            user_input=[
                sparkapi_pb2.AddColumnExpression(
                    new_column_name=user_input.get('new_column_name', ''),
                    expression=sparkapi_pb2.Expression(
                        method_name=user_input['expression'].get('method_name', ''),
                        return_value_type=user_input['expression'].get('return_value_type', ''),
                        compiled=user_input['expression'].get('compiled', ''),
                        params=[sparkapi_pb2.Param(**params) for params in user_input['expression'].get('params', [])],
                    ),
                )
                for user_input in request_data.get('user_input', [])
            ],
        )

        for response in rpc_client.client.submit_AddColumnNode(request):
            response: sparkapi_pb2.SparkTransformResponse
            yield {
                'session_id': response.session_id,
                'node_id': response.node_id,
                'prev_node_id': response.prev_node_id,
                'invalid_state': {
                    'active': response.invalid_state.active,
                    'error_msg': response.invalid_state.error_msg,
                },
                'active': response.active,
                'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns],
                'title': response.title,
                'user_input': response.user_input,
            }

    except grpc.RpcError as e:
        raise ApplicationError(message=str(e), code=500) from e


def toggle_node(request_data: dict[str, Any]) -> Iterator[dict[str, Any]]:
    """Toggle a node with streaming response."""
    try:
        request = sparkapi_pb2.NodeToggleRequest(**request_data)
        for response in rpc_client.client.toggleNode(request):
            response: sparkapi_pb2.SparkTransformResponse
            yield {
                'session_id': response.session_id,
                'node_id': response.node_id,
                'prev_node_id': response.prev_node_id,
                'invalid_state': {
                    'active': response.invalid_state.active,
                    'error_msg': response.invalid_state.error_msg,
                },
                'active': response.active,
                'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns],
                'title': response.title,
                'user_input': response.user_input,
            }
    except grpc.RpcError as e:
        raise ApplicationError(message=str(e), code=500) from e


def remove_node(request_data: dict[str, Any]) -> Iterator[dict[str, Any]]:
    """Remove a node with streaming response."""
    try:
        request = sparkapi_pb2.NodeRemovalRequest(**request_data)
        for response in rpc_client.client.removeNode(request):
            response: sparkapi_pb2.SparkTransformResponse
            yield {
                'session_id': response.session_id,
                'node_id': response.node_id,
                'prev_node_id': response.prev_node_id,
                'invalid_state': {
                    'active': response.invalid_state.active,
                    'error_msg': response.invalid_state.error_msg,
                },
                'active': response.active,
                'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns],
                'title': response.title,
                'user_input': response.user_input,
            }

    except grpc.RpcError as e:
        raise ApplicationError(message=str(e), code=500) from e


def submit_load_from_session_node(request_data: dict[str, Any]) -> dict[str, Any]:
    """Submit load from session node."""
    try:
        request = sparkapi_pb2.LoadFromSessionNodeRequest(**request_data)
        response: sparkapi_pb2.SparkTransformResponse = rpc_client.client.submit_LoadFromSessionNode(request)
        return {
            'session_id': response.session_id,
            'node_id': response.node_id,
            'prev_node_id': response.prev_node_id,
            'invalid_state': {
                'active': response.invalid_state.active,
                'error_msg': response.invalid_state.error_msg,
            },
            'active': response.active,
            'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns],
            'title': response.title,
            'user_input': response.user_input,
        }
    except grpc.RpcError as e:
        raise ApplicationError(message=str(e), code=500) from e


def submit_filter_node(request_data: dict[str, Any]) -> dict[str, Any]:
    """Submit filter node."""
    try:
        request = sparkapi_pb2.FilterNodeRequest(
            session_id=request_data.get('session_id', ''),
            node_id=request_data.get('node_id', ''),
            prev_node_id=request_data.get('prev_node_id', ''),
            matching=request_data.get('matching', ''),
            expressions=[expr for expr in request_data.get('expressions', [])],
        )
        response: sparkapi_pb2.SparkTransformResponse = rpc_client.client.submit_FilterNode(request)
        return {
            'session_id': response.session_id,
            'node_id': response.node_id,
            'prev_node_id': response.prev_node_id,
            'invalid_state': {
                'active': response.invalid_state.active,
                'error_msg': response.invalid_state.error_msg,
            },
            'active': response.active,
            'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns],
            'title': response.title,
            'user_input': response.user_input,
        }
    except grpc.RpcError as e:
        raise ApplicationError(message=str(e), code=500) from e


def submit_join_node(request_data: dict[str, Any]) -> dict[str, Any]:
    """Submit join node."""
    try:
        request = sparkapi_pb2.JoinNodeRequest(
            session_id=request_data.get('session_id', ''),
            node_id=request_data.get('node_id', ''),
            prev_node_id=request_data.get('prev_node_id', ''),
            csv=sparkapi_pb2.CsvInput(**request_data['csv']) if request_data.get('csv') else None,
            json=sparkapi_pb2.JsonInput(**request_data['json']) if request_data.get('json') else None,
            parquet=sparkapi_pb2.ParquetInput(**request_data['parquet']) if request_data.get('parquet') else None,
            session=sparkapi_pb2.SessionInput(**request_data['session']) if request_data.get('session') else None,
            joinParams=sparkapi_pb2.JoinParams(
                join_relation=request_data['joinParams'].get('join_relation', ''),
                prefix_for_added_columns=request_data['joinParams'].get('prefix_for_added_columns', ''),
                criteria_matching=request_data['joinParams'].get('criteria_matching', ''),
                columns_to_keep=[col for col in request_data['joinParams'].get('columns_to_keep', [])],
                columns_to_add=[col for col in request_data['joinParams'].get('columns_to_add', [])],
                join_criteria=[criteria for criteria in request_data['joinParams'].get('join_criteria', [])],
            ),
        )
        response: sparkapi_pb2.SparkTransformResponse = rpc_client.client.submit_JoinNode(request)
        return {
            'session_id': response.session_id,
            'node_id': response.node_id,
            'prev_node_id': response.prev_node_id,
            'invalid_state': {
                'active': response.invalid_state.active,
                'error_msg': response.invalid_state.error_msg,
            },
            'active': response.active,
            'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns],
            'title': response.title,
            'user_input': response.user_input,
        }
    except grpc.RpcError as e:
        raise ApplicationError(message=str(e), code=500) from e


def submit_table_node(request_data: dict[str, Any]) -> dict[str, Any]:
    """Submit table node."""
    try:
        request = sparkapi_pb2.AddTableNodeRequest(**request_data)
        response: sparkapi_pb2.SparkTransformResponse = rpc_client.client.submit_TableNode(request)
        return {
            'session_id': response.session_id,
            'node_id': response.node_id,
            'prev_node_id': response.prev_node_id,
            'invalid_state': {
                'active': response.invalid_state.active,
                'error_msg': response.invalid_state.error_msg,
            },
            'active': response.active,
            'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns],
            'title': response.title,
            'user_input': response.user_input,
        }
    except grpc.RpcError as e:
        raise ApplicationError(message=str(e), code=500) from e


def submit_histogram_node(request_data: dict[str, Any]) -> dict[str, Any]:
    """Submit histogram node."""
    try:
        request = sparkapi_pb2.AddHistogramNodeRequest(**request_data)
        response: sparkapi_pb2.SparkTransformResponse = rpc_client.client.submit_HistogramNode(request)
        return {
            'session_id': response.session_id,
            'node_id': response.node_id,
            'prev_node_id': response.prev_node_id,
            'invalid_state': {
                'active': response.invalid_state.active,
                'error_msg': response.invalid_state.error_msg,
            },
            'active': response.active,
            'columns': [{'name': col.name, 'dtype': col.dtype} for col in response.columns],
            'title': response.title,
            'user_input': response.user_input,
        }
    except grpc.RpcError as e:
        raise ApplicationError(message=str(e), code=500) from e
