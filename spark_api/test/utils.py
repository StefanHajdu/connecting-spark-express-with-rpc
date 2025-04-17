import requests
from spark_api.src.custom_exceptions import DuplicateSessionException, NodeMissingException

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
    res = requests.post('http://localhost:4444/createSession', json=json_data)

    assert res.status_code == 200 or (res.status_code == 500 and duplicateSessionException.__str__() in res.json()['error']['message'])
    return session_id


def submit_loadNode(session_id: str, src_path: str, src_type: str) -> None:
    json_data = {
        'session_id': session_id,
        'df_path': src_path,
        'df_type': src_type,
    }
    res = requests.post('http://localhost:4444/submitNode/LoadDatasetNode', json=json_data)

    assert res.status_code == 200


def submit_loadFromSessionNode(session_id: str, input_session_id: str) -> None:
    json_data = {
        'session_id': session_id,
        'input_session_id': input_session_id,
    }
    res = requests.post('http://localhost:4444/submitNode/LoadFromSessionNode', json=json_data)

    assert res.status_code == 200


def submit_filterNode(**kwargs) -> str:
    res = requests.post('http://localhost:4444/submitNode/FilterNode', json=kwargs)

    assert res.status_code == 200
    return kwargs['node_id']


def submit_newColumnNode(**kwargs) -> str:
    res = requests.post('http://localhost:4444/submitNode/NewColumnNode', json=kwargs)

    assert res.status_code == 200
    return kwargs['node_id']


def submit_joinNode(**kwargs) -> str:
    res = requests.post('http://localhost:4444/submitNode/JoinNode', json=kwargs)

    assert res.status_code == 200
    return kwargs['node_id']


def removeNode(**kwargs):
    res = requests.post('http://localhost:4444/removeNode', json=kwargs)

    assert res.status_code == 200


def summarize(session_id: str, node_id: str) -> dict:
    json_data = {
        'session_id': session_id,
        'node_id': node_id,
    }
    res = requests.post('http://localhost:4444/summarize', json=json_data)

    assert res.status_code == 200 or (res.status_code == 500 and nodeMissingException.__str__() in res.json()['error']['message'])
    return res.json()


def get_rebuild_status(session_id: str) -> bool:
    res = requests.get(f'http://localhost:4444/getSessionStatus/{session_id}')

    assert res.status_code == 200
    return res.json()['rebuild_recommendation']


def rebuild_session(session_id: str):
    res = requests.post(f'http://localhost:4444/rebuildSession/{session_id}')

    assert res.status_code == 200
