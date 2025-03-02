import requests

from spark_api.src.session_exceptions import DuplicateSessionException

duplicateSessionException = DuplicateSessionException()


def create_session(session_id: str):
    json_data = {
        "id": session_id,
    }

    res = requests.post("http://localhost:4444/createSession", json=json_data)
    assert res.status_code == 200 or (
        res.status_code == 500 and duplicateSessionException.__str__() in res.json()["error"]["message"]
    )
    return session_id


def load(session_id: str, src_path: str, src_type: str):
    json_data = {
        "session_id": session_id,
        "df_path": src_path,
        "df_type": src_type,
    }

    res = requests.post("http://localhost:4444/load", json=json_data)
    assert res.status_code == 200


def load_from_session(session_id: str, input_session_id: str):
    json_data = {
        "session_id": session_id,
        "input_id": input_session_id,
    }

    res = requests.post("http://localhost:4444/loadFromSession", json=json_data)
    assert res.status_code == 200


def add_sql(**kwargs):
    res = requests.post("http://localhost:4444/addSql", json=kwargs)
    assert res.status_code == 200
    return kwargs["node_id"]


def summarize(session_id: str, node_id: str):
    json_data = {
        "session_id": session_id,
        "node_id": node_id,
    }

    res = requests.post("http://localhost:4444/summarize", json=json_data)
    assert res.status_code == 200
    return res.json()
