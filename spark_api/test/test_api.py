import json
import uuid

import pytest
import requests
from state import TestState

import utils as u

TEST_STATE = TestState()
DEFAULT_SESSION_ID = '00000'


def session(my_id: str) -> str:
    return u.create_session(session_id=my_id)


def add_some_columns(session_id):
    node_id_1 = u.submit_newColumnNode(
        **{
            'session_id': session_id,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'expressions': [{'expression': 'upper(domain)', 'col_name': 'a2'}],
        }
    )

    _ = u.submit_newColumnNode(
        **{
            'session_id': session_id,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_id_1,
            'expressions': [{'expression': 'upper(tld)', 'col_name': 'b2'}],
        }
    )


@pytest.mark.parametrize(
    'session_id, node_request_body, expected',
    [
        (
            u.to_session_id(1),
            {
                'session_id': u.to_session_id(1),
                'node_id': u.to_node_id(5),
                'prev_node_id': TEST_STATE.root_node_id,
                'expressions': [{'expression': 'upper(domain)', 'col_name': 'x'}],
            },
            [
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'date'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'date'},
                        {'name': 'x', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(1),
                    'node_id': u.to_node_id(5),
                    'invalid_state': {'active': False, 'error_msg': ''},
                },
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'date'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'date'},
                        {'name': 'x', 'dtype': 'string'},
                        {'name': 'a2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(1),
                    'node_id': u.to_node_id(1),
                    'invalid_state': {'active': False, 'error_msg': ''},
                },
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'date'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'date'},
                        {'name': 'x', 'dtype': 'string'},
                        {'name': 'a2', 'dtype': 'string'},
                        {'name': 'b2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(1),
                    'node_id': u.to_node_id(2),
                    'invalid_state': {'active': False, 'error_msg': ''},
                },
            ],
        ),
        (
            u.to_session_id(2),
            {
                'session_id': u.to_session_id(2),
                'node_id': u.to_node_id(5),
                'prev_node_id': u.to_node_id(1),
                'expressions': [{'expression': 'upper(domain)', 'col_name': 'x'}],
            },
            [
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'date'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'date'},
                        {'name': 'a2', 'dtype': 'string'},
                        {'name': 'x', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(2),
                    'node_id': u.to_node_id(5),
                    'invalid_state': {'active': False, 'error_msg': ''},
                },
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'date'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'date'},
                        {'name': 'a2', 'dtype': 'string'},
                        {'name': 'x', 'dtype': 'string'},
                        {'name': 'b2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(2),
                    'node_id': u.to_node_id(2),
                    'invalid_state': {'active': False, 'error_msg': ''},
                },
            ],
        ),
        (
            u.to_session_id(3),
            {
                'session_id': u.to_session_id(3),
                'node_id': u.to_node_id(5),
                'prev_node_id': u.to_node_id(2),
                'expressions': [{'expression': 'upper(domain)', 'col_name': 'x'}],
            },
            [
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'date'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'date'},
                        {'name': 'a2', 'dtype': 'string'},
                        {'name': 'b2', 'dtype': 'string'},
                        {'name': 'x', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(3),
                    'node_id': u.to_node_id(5),
                    'invalid_state': {'active': False, 'error_msg': ''},
                },
            ],
        ),
    ],
)
def test_column_adding(session_id, node_request_body, expected):
    _ = session(session_id)
    _ = u.submit_loadNode({'session_id': session_id, 'csv': {'delimiter': ';', 'include_header': True, 'path': TEST_STATE.path}})
    add_some_columns(session_id)

    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/submitNewColumnNode', json=node_request_body)

    assert res.status_code == 200

    for a, b in zip(res.json(), expected):
        assert json.dumps(a) == json.dumps(b)
