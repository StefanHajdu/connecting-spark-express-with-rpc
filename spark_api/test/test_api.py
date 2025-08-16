import json

import pytest
import requests
from state import TestState

import utils as u

TEST_STATE = TestState()


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


def add_column_dependency(session_id):
    _ = requests.post(
        'http://localhost:4444/rpc/sessionNode/transform/submitNewColumnNode',
        json={
            'session_id': session_id,
            'node_id': u.to_node_id(5),
            'prev_node_id': TEST_STATE.root_node_id,
            'expressions': [{'expression': 'upper(domain)', 'col_name': 'x'}],
        },
    )
    _ = requests.post(
        'http://localhost:4444/rpc/sessionNode/transform/submitNewColumnNode',
        json={
            'session_id': session_id,
            'node_id': u.to_node_id(1),
            'prev_node_id': u.to_node_id(5),
            'expressions': [{'expression': 'upper(x)', 'col_name': 'a2'}],
        },
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
                    'active': True,
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
                    'active': True,
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
                    'active': True,
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
                    'active': True,
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
                    'active': True,
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
                    'active': True,
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


@pytest.mark.parametrize(
    'session_id, removal_request_body, expected',
    [
        (
            u.to_session_id(3),
            {
                'session_id': u.to_session_id(3),
                'node_id': u.to_node_id(1),
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
                        {'name': 'b2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(3),
                    'node_id': u.to_node_id(2),
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                }
            ],
        ),
        (
            u.to_session_id(4),
            {
                'session_id': u.to_session_id(4),
                'node_id': u.to_node_id(2),
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
                    ],
                    'session_id': u.to_session_id(4),
                    'node_id': u.to_node_id(1),
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                }
            ],
        ),
    ],
)
def test_column_removing(session_id, removal_request_body, expected):
    _ = session(session_id)
    _ = u.submit_loadNode({'session_id': session_id, 'csv': {'delimiter': ';', 'include_header': True, 'path': TEST_STATE.path}})
    add_some_columns(session_id)

    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/removeNode', json=removal_request_body)

    assert res.status_code == 200

    for a, b in zip(res.json(), expected):
        assert json.dumps(a) == json.dumps(b)


@pytest.mark.parametrize(
    'session_id, removal_request_body, expected',
    [
        (
            u.to_session_id(5),
            {
                'session_id': u.to_session_id(5),
                'node_id': u.to_node_id(5),
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
                        {'name': 'a2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(5),
                    'node_id': u.to_node_id(1),
                    'invalid_state': {
                        'active': True,
                        'error_msg': "UNRESOLVED_COLUMN.WITH_SUGGESTION with {'objectName': '`x`', 'proposal': '`tld`, `dnssec`, `domain`, `registrar`, `created_at`'} in node: node_0001",
                    },
                    'active': True,
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
                    'session_id': u.to_session_id(5),
                    'node_id': u.to_node_id(2),
                    'invalid_state': {
                        'active': True,
                        'error_msg': "UNRESOLVED_COLUMN.WITH_SUGGESTION with {'objectName': '`x`', 'proposal': '`tld`, `dnssec`, `domain`, `registrar`, `created_at`'} in node: node_0002",
                    },
                    'active': True,
                },
            ],
        ),
    ],
)
def test_column_removing_and_checking_invalid_status(session_id, removal_request_body, expected):
    _ = session(session_id)
    _ = u.submit_loadNode({'session_id': session_id, 'csv': {'delimiter': ';', 'include_header': True, 'path': TEST_STATE.path}})
    add_some_columns(session_id)
    add_column_dependency(session_id)

    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/removeNode', json=removal_request_body)

    assert res.status_code == 200

    for a, b in zip(res.json(), expected):
        assert json.dumps(a) == json.dumps(b)
