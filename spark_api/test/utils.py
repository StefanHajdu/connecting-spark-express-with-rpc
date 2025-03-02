import requests

from spark_api.src.session_exceptions import DuplicateSessionException

duplicateSessionException = DuplicateSessionException()


def to_session_id(id: int):
    return "session_" + str(id).zfill(4)


def to_node_id(id: int):
    return "node_" + str(id).zfill(4)


def create_session(session_id: str) -> str:
    json_data = {
        "id": session_id,
    }
    res = requests.post("http://localhost:4444/createSession", json=json_data)

    assert res.status_code == 200 or (
        res.status_code == 500 and duplicateSessionException.__str__() in res.json()["error"]["message"]
    )
    return session_id


def load(session_id: str, src_path: str, src_type: str) -> None:
    json_data = {
        "session_id": session_id,
        "df_path": src_path,
        "df_type": src_type,
    }
    res = requests.post("http://localhost:4444/load", json=json_data)

    assert res.status_code == 200


def load_from_session(session_id: str, input_session_id: str) -> None:
    json_data = {
        "session_id": session_id,
        "input_id": input_session_id,
    }
    res = requests.post("http://localhost:4444/loadFromSession", json=json_data)

    assert res.status_code == 200


def add_sql(**kwargs) -> str:
    res = requests.post("http://localhost:4444/addSql", json=kwargs)

    assert res.status_code == 200
    return kwargs["node_id"]


def summarize(session_id: str, node_id: str) -> dict:
    json_data = {
        "session_id": session_id,
        "node_id": node_id,
    }
    res = requests.post("http://localhost:4444/summarize", json=json_data)

    assert res.status_code == 200
    return res.json()


def get_rebuild_status(session_id: str) -> bool:
    res = requests.get(f"http://localhost:4444/rebuildStatus/{session_id}")

    assert res.status_code == 200
    return res.json()["rebuild_status"]


def rebuild_session(session_id: str):
    res = requests.post(f"http://localhost:4444/rebuildSession/{session_id}")

    assert res.status_code == 200
