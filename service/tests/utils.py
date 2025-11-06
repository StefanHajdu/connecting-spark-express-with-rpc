import json
import sys
from pathlib import Path

import requests

# Add the service directory to Python path
service_dir = Path(__file__).parent.parent
sys.path.insert(0, str(service_dir))

from core.exceptions import DuplicateSessionException, NodeMissingException  # noqa: E402

nodeMissingException = NodeMissingException()
duplicateSessionException = DuplicateSessionException()


def parse_streaming_json_response(response: requests.Response):
    """Parse streaming JSON response from FastAPI StreamingResponse."""
    result = []
    for line in response.iter_lines():
        if line:
            try:
                result.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return result


def to_session_id(session_id: int):
    return 'session_' + str(session_id).zfill(4)


def to_node_id(session_id: int):
    return 'node_' + str(session_id).zfill(4)


def create_session(session_id: str) -> str:
    json_data = {'session_id': session_id, 'name': 'random_name'}
    res = requests.post('http://localhost:4444/rpc/session/create', json=json_data)

    assert res.status_code == 200 or (res.status_code == 500 and duplicateSessionException.__str__() in res.json()['error']['message'])
    return session_id


def submit_loadNode(json_data: dict) -> list:
    res = requests.post('http://localhost:4444/rpc/node/submitLoadDatasetNode', json=json_data, stream=True)

    assert res.status_code == 200
    return parse_streaming_json_response(res)


def submit_loadFromSessionNode(session_id: str, input_session_id: str) -> None:
    json_data = {
        'session_id': session_id,
        'input_session_id': input_session_id,
    }
    res = requests.post('http://localhost:4444/rpc/node/submitLoadFromSessionNode', json=json_data)

    assert res.status_code == 200


def submit_filterNode(**kwargs) -> str:
    res = requests.post('http://localhost:4444/rpc/node/submitFilterNode', json=kwargs)

    assert res.status_code == 200
    return kwargs['node_id']


def submit_newColumnNode(**kwargs) -> str:
    res = requests.post('http://localhost:4444/rpc/node/submitAddColumnNode', json=kwargs, stream=True)

    assert res.status_code == 200
    # Wait for the streaming response to complete to ensure node is fully created
    result = parse_streaming_json_response(res)

    assert 'node_id' in result[0], f'Failed to create node: {result}'
    return kwargs['node_id']


def submit_joinNode(**kwargs) -> str:
    res = requests.post('http://localhost:4444/rpc/node/submitJoinNode', json=kwargs)

    assert res.status_code == 200
    return kwargs['node_id']


def removeNode(**kwargs):
    res = requests.post('http://localhost:4444/rpc/node/removeNode', json=kwargs, stream=True)

    assert res.status_code == 200
    return parse_streaming_json_response(res)


def toggleNode(**kwargs):
    res = requests.post('http://localhost:4444/rpc/node/toggleNode', json=kwargs, stream=True)

    assert res.status_code == 200
    return parse_streaming_json_response(res)


def summarize(session_id: str, node_id: str) -> dict:
    json_data = {
        'session_id': session_id,
        'node_id': node_id,
    }
    res = requests.post('http://localhost:4444/rpc/node/summarize', json=json_data)

    assert res.status_code == 200 or (res.status_code == 500 and nodeMissingException.__str__() in res.json()['error']['message'])
    return res.json()


def get_rebuild_status(session_id: str) -> bool:
    res = requests.get(f'http://localhost:4444/rpc/session/status/{session_id}')

    assert res.status_code == 200
    return res.json()['rebuild_recommendation']


def rebuild_session(session_id: str):
    res = requests.post(f'http://localhost:4444/rpc/session/rebuild/{session_id}')

    assert res.status_code == 200
