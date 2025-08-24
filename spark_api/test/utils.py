import requests

from exceptions import DuplicateSessionException, NodeMissingException

nodeMissingException = NodeMissingException()
duplicateSessionException = DuplicateSessionException()


def to_session_id(id: int):
    return 'session_' + str(id).zfill(4)


def to_node_id(id: int):
    return 'node_' + str(id).zfill(4)


def create_session(session_id: str) -> str:
    json_data = {
        'id': session_id,
    }
    res = requests.post('http://localhost:4444/rpc/session/create', json=json_data)

    assert res.status_code == 200 or (res.status_code == 500 and duplicateSessionException.__str__() in res.json()['error']['message'])
    return session_id


def submit_loadNode(json_data: dict) -> None:
    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/submitLoadDatasetNode', json=json_data)

    assert res.status_code == 200


def submit_loadFromSessionNode(session_id: str, input_session_id: str) -> None:
    json_data = {
        'session_id': session_id,
        'input_session_id': input_session_id,
    }
    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/submitLoadFromSessionNode', json=json_data)

    assert res.status_code == 200


def submit_filterNode(**kwargs) -> str:
    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/submitFilterNode', json=kwargs)

    assert res.status_code == 200
    return kwargs['node_id']


def submit_newColumnNode(**kwargs) -> str:
    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/submitAddColumnNode', json=kwargs)

    assert res.status_code == 200
    return kwargs['node_id']


def submit_joinNode(**kwargs) -> str:
    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/submitJoinNode', json=kwargs)

    assert res.status_code == 200
    return kwargs['node_id']


def removeNode(**kwargs):
    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/removeNode', json=kwargs)

    assert res.status_code == 200


def toggleNode(**kwargs):
    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/toggleNode', json=kwargs)

    assert res.status_code == 200


def summarize(session_id: str, node_id: str) -> dict:
    json_data = {
        'session_id': session_id,
        'node_id': node_id,
    }
    res = requests.post('http://localhost:4444/rpc/sessionNode/action/summarize', json=json_data)

    assert res.status_code == 200 or (res.status_code == 500 and nodeMissingException.__str__() in res.json()['error']['message'])
    return res.json()


def get_rebuild_status(session_id: str) -> bool:
    res = requests.get(f'http://localhost:4444/rpc/session/status/{session_id}')

    assert res.status_code == 200
    return res.json()['rebuild_recommendation']


def rebuild_session(session_id: str):
    res = requests.post(f'http://localhost:4444/rpc/session/rebuild/{session_id}')

    assert res.status_code == 200
