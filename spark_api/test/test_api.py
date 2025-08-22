import json

import pytest
import requests
from state import CURRENT_DIR, TestState

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
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
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
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
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
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
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
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
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
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
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
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
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
    _ = u.submit_loadNode({'session_id': session_id, 'parquet': {'path': TEST_STATE.path}})
    add_some_columns(session_id)

    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/submitNewColumnNode', json=node_request_body)

    assert res.status_code == 200

    for a, b in zip(res.json(), expected, strict=True):
        assert json.dumps(a) == json.dumps(b)


@pytest.mark.parametrize(
    'session_id, removal_request_body, expected',
    [
        (
            u.to_session_id(30),
            {
                'session_id': u.to_session_id(30),
                'node_id': u.to_node_id(1),
            },
            [
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                        {'name': 'b2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(30),
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
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
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
    _ = u.submit_loadNode({'session_id': session_id, 'parquet': {'path': TEST_STATE.path}})
    add_some_columns(session_id)

    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/removeNode', json=removal_request_body)

    assert res.status_code == 200

    for a, b in zip(res.json(), expected, strict=True):
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
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                        {'name': 'x', 'dtype': 'string'},
                        {'name': 'a2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(5),
                    'node_id': u.to_node_id(1),
                    'invalid_state': {
                        'active': True,
                        'error_msg': "UNRESOLVED_COLUMN.WITH_SUGGESTION with {'objectName': '`x`', 'proposal': '`tld`, `dnssec`, `domain`, `registrar`, `created_at`'} in node: node_0001",  # noqa
                    },
                    'active': True,
                },
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                        {'name': 'x', 'dtype': 'string'},
                        {'name': 'a2', 'dtype': 'string'},
                        {'name': 'b2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(5),
                    'node_id': u.to_node_id(2),
                    'invalid_state': {
                        'active': True,
                        'error_msg': "UNRESOLVED_COLUMN.WITH_SUGGESTION with {'objectName': '`x`', 'proposal': '`tld`, `dnssec`, `domain`, `registrar`, `created_at`'} in node: node_0001",  # noqa
                    },
                    'active': True,
                },
            ],
        ),
    ],
)
def test_columns_removal_and_check_invalid_status(session_id, removal_request_body, expected):
    _ = session(session_id)
    _ = u.submit_loadNode({'session_id': session_id, 'parquet': {'path': TEST_STATE.path}})
    add_some_columns(session_id)
    add_column_dependency(session_id)

    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/removeNode', json=removal_request_body)

    assert res.status_code == 200

    for a, b in zip(res.json(), expected, strict=True):
        assert json.dumps(a) == json.dumps(b)


@pytest.mark.parametrize(
    'session_id, toggle_request_body, expected',
    [
        (
            u.to_session_id(6),
            {'session_id': u.to_session_id(6), 'node_id': u.to_node_id(1), 'active': False},
            [
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(6),
                    'node_id': u.to_node_id(1),
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': False,
                },
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                        {'name': 'b2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(6),
                    'node_id': u.to_node_id(2),
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                },
            ],
        ),
        (
            u.to_session_id(7),
            {'session_id': u.to_session_id(7), 'node_id': u.to_node_id(2), 'active': False},
            [
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                        {'name': 'a2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(7),
                    'node_id': u.to_node_id(2),
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': False,
                }
            ],
        ),
    ],
)
def test_node_disable(session_id, toggle_request_body, expected):
    _ = session(session_id)
    _ = u.submit_loadNode({'session_id': session_id, 'parquet': {'path': TEST_STATE.path}})
    add_some_columns(session_id)

    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/toggleNode', json=toggle_request_body)

    assert res.status_code == 200

    for a, b in zip(res.json(), expected, strict=True):
        assert json.dumps(a) == json.dumps(b)


@pytest.mark.parametrize(
    'session_id, add_dependecy, toggle_request_body, expected_excluded, expected_included',
    [
        (
            u.to_session_id(8),
            True,
            {'session_id': u.to_session_id(8), 'node_id': u.to_node_id(5), 'toggle': False},
            [
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(8),
                    'node_id': u.to_node_id(5),
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': False,
                },
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                        {'name': 'x', 'dtype': 'string'},
                        {'name': 'a2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(8),
                    'node_id': u.to_node_id(1),
                    'invalid_state': {
                        'active': True,
                        'error_msg': "UNRESOLVED_COLUMN.WITH_SUGGESTION with {'objectName': '`x`', 'proposal': '`tld`, `dnssec`, `domain`, `registrar`, `created_at`'} in node: node_0001",  # noqa
                    },
                    'active': True,
                },
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                        {'name': 'x', 'dtype': 'string'},
                        {'name': 'a2', 'dtype': 'string'},
                        {'name': 'b2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(8),
                    'node_id': u.to_node_id(2),
                    'invalid_state': {
                        'active': True,
                        'error_msg': "UNRESOLVED_COLUMN.WITH_SUGGESTION with {'objectName': '`x`', 'proposal': '`tld`, `dnssec`, `domain`, `registrar`, `created_at`'} in node: node_0001",  # noqa
                    },
                    'active': True,
                },
            ],
            [
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                        {'name': 'x', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(8),
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
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                        {'name': 'x', 'dtype': 'string'},
                        {'name': 'a2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(8),
                    'node_id': u.to_node_id(1),
                    'invalid_state': {
                        'active': False,
                        'error_msg': '',
                    },
                    'active': True,
                },
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                        {'name': 'x', 'dtype': 'string'},
                        {'name': 'a2', 'dtype': 'string'},
                        {'name': 'b2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(8),
                    'node_id': u.to_node_id(2),
                    'invalid_state': {
                        'active': False,
                        'error_msg': '',
                    },
                    'active': True,
                },
            ],
        ),
    ],
)
def test_node_toggle(session_id, add_dependecy, toggle_request_body, expected_excluded, expected_included):
    _ = session(session_id)
    _ = u.submit_loadNode({'session_id': session_id, 'parquet': {'path': TEST_STATE.path}})
    add_some_columns(session_id)

    if add_dependecy:
        add_column_dependency(session_id)

    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/toggleNode', json=toggle_request_body)
    assert res.status_code == 200
    for a, b in zip(res.json(), expected_excluded, strict=True):
        assert json.dumps(a) == json.dumps(b)

    toggle_request_body['toggle'] = True
    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/toggleNode', json=toggle_request_body)
    assert res.status_code == 200
    for a, b in zip(res.json(), expected_included, strict=True):
        assert json.dumps(a) == json.dumps(b)


@pytest.mark.parametrize(
    'session_id, path_replace_request_body, expected',
    [
        (
            u.to_session_id(9),
            {'session_id': u.to_session_id(9), 'json': {'multiline': True, 'path': f'{CURRENT_DIR}/../../data/df2.json'}},
            [
                {
                    'columns': [{'name': 'id', 'dtype': 'long'}, {'name': 'name', 'dtype': 'string'}],
                    'session_id': u.to_session_id(9),
                    'node_id': TEST_STATE.root_node_id,
                    'invalid_state': {
                        'active': False,
                        'error_msg': '',
                    },
                    'active': True,
                },
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                        {'name': 'a2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(9),
                    'node_id': u.to_node_id(1),
                    'invalid_state': {
                        'active': True,
                        'error_msg': "UNRESOLVED_COLUMN.WITH_SUGGESTION with {'objectName': '`domain`', 'proposal': '`id`, `name`'} in node: node_0001",  # noqa
                    },
                    'active': True,
                },
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                        {'name': 'a2', 'dtype': 'string'},
                        {'name': 'b2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(9),
                    'node_id': u.to_node_id(2),
                    'invalid_state': {
                        'active': True,
                        'error_msg': "UNRESOLVED_COLUMN.WITH_SUGGESTION with {'objectName': '`domain`', 'proposal': '`id`, `name`'} in node: node_0001",  # noqa
                    },
                    'active': True,
                },
            ],
        ),
        (
            u.to_session_id(90),
            {'session_id': u.to_session_id(90), 'parquet': {'path': TEST_STATE.path}},
            [
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(90),
                    'node_id': TEST_STATE.root_node_id,
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                },
                {
                    'columns': [
                        {'name': 'domain', 'dtype': 'string'},
                        {'name': 'tld', 'dtype': 'string'},
                        {'name': 'dnssec', 'dtype': 'string'},
                        {'name': 'registrar', 'dtype': 'string'},
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                        {'name': 'a2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(90),
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
                        {'name': 'created_at', 'dtype': 'string'},
                        {'name': 'records_ns', 'dtype': 'string'},
                        {'name': 'records_ds', 'dtype': 'string'},
                        {'name': 'records_dnskey', 'dtype': 'string'},
                        {'name': 'analyzed_at', 'dtype': 'string'},
                        {'name': 'a2', 'dtype': 'string'},
                        {'name': 'b2', 'dtype': 'string'},
                    ],
                    'session_id': u.to_session_id(90),
                    'node_id': u.to_node_id(2),
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                },
            ],
        ),
    ],
)
def test_input_path_replace(session_id, path_replace_request_body, expected):
    _ = session(session_id)
    _ = u.submit_loadNode({'session_id': session_id, 'parquet': {'path': TEST_STATE.path}})
    add_some_columns(session_id)

    res = requests.post('http://localhost:4444/rpc/sessionNode/transform/submitLoadDatasetNode', json=path_replace_request_body)
    assert res.status_code == 200

    for a, b in zip(res.json(), expected, strict=True):
        assert json.dumps(a) == json.dumps(b)
