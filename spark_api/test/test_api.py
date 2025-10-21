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
            'user_input': [{'expression': {'compiled': 'upper(domain) as a2', 'method_name': 'upper', 'params': []}}],
        }
    )

    _ = u.submit_newColumnNode(
        **{
            'session_id': session_id,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_id_1,
            'user_input': [{'expression': {'compiled': 'upper(tld) as b2', 'method_name': 'upper', 'params': []}}],
        }
    )


def add_column_dependency(session_id):
    _ = requests.post(
        'http://localhost:4444/rpc/node/submitAddColumnNode',
        json={
            'session_id': session_id,
            'node_id': u.to_node_id(5),
            'prev_node_id': TEST_STATE.root_node_id,
            'user_input': [{'expression': {'compiled': 'upper(domain) as x', 'method_name': 'upper', 'params': []}}],
        },
    )
    _ = requests.post(
        'http://localhost:4444/rpc/node/submitAddColumnNode',
        json={
            'session_id': session_id,
            'node_id': u.to_node_id(1),
            'prev_node_id': u.to_node_id(5),
            'user_input': [{'expression': {'compiled': 'upper(x) as a2', 'method_name': 'upper', 'params': []}}],
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
                'user_input': [{'expression': {'compiled': 'upper(domain) as x', 'method_name': 'upper', 'params': []}}],
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
                    'prev_node_id': TEST_STATE.root_node_id,
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
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
                    'prev_node_id': u.to_node_id(5),
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
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
                    'prev_node_id': u.to_node_id(1),
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
                },
            ],
        ),
        (
            u.to_session_id(2),
            {
                'session_id': u.to_session_id(2),
                'node_id': u.to_node_id(5),
                'prev_node_id': u.to_node_id(1),
                'user_input': [{'expression': {'compiled': 'upper(domain) as x', 'method_name': 'upper', 'params': [], 'new_column_name': 'x'}}],
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
                    'prev_node_id': u.to_node_id(1),
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
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
                    'prev_node_id': u.to_node_id(5),
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
                },
            ],
        ),
        (
            u.to_session_id(3),
            {
                'session_id': u.to_session_id(3),
                'node_id': u.to_node_id(5),
                'prev_node_id': u.to_node_id(2),
                'user_input': [{'expression': {'compiled': 'upper(domain) as x', 'method_name': 'upper', 'params': [], 'new_column_name': 'x'}}],
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
                    'prev_node_id': u.to_node_id(2),
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
                },
            ],
        ),
    ],
)
def test_column_adding(session_id, node_request_body, expected):
    _ = session(session_id)
    _ = u.submit_loadNode({'session_id': session_id, 'parquet': {'path': TEST_STATE.path}})
    add_some_columns(session_id)

    res = requests.post('http://localhost:4444/rpc/node/submitAddColumnNode', json=node_request_body)

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
                    'prev_node_id': TEST_STATE.root_node_id,
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
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
                    'prev_node_id': TEST_STATE.root_node_id,
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
                }
            ],
        ),
    ],
)
def test_column_removing(session_id, removal_request_body, expected):
    _ = session(session_id)
    _ = u.submit_loadNode({'session_id': session_id, 'parquet': {'path': TEST_STATE.path}})
    add_some_columns(session_id)

    res = requests.post('http://localhost:4444/rpc/node/removeNode', json=removal_request_body)

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
                    'prev_node_id': TEST_STATE.root_node_id,
                    'invalid_state': {
                        'active': True,
                        'error_msg': "UNRESOLVED_COLUMN.WITH_SUGGESTION with {'objectName': '`x`', 'proposal': '`tld`, `dnssec`, `domain`, `registrar`, `created_at`'} in node: node_0001",  # noqa
                    },
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
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
                    'prev_node_id': u.to_node_id(1),
                    'invalid_state': {
                        'active': True,
                        'error_msg': "UNRESOLVED_COLUMN.WITH_SUGGESTION with {'objectName': '`x`', 'proposal': '`tld`, `dnssec`, `domain`, `registrar`, `created_at`'} in node: node_0001",  # noqa
                    },
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
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

    res = requests.post('http://localhost:4444/rpc/node/removeNode', json=removal_request_body)

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
                    'prev_node_id': TEST_STATE.root_node_id,
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': False,
                    'title': 'AddColumnNode',
                    'user_input': '',
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
                    'prev_node_id': u.to_node_id(1),
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
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
                    'prev_node_id': u.to_node_id(1),
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': False,
                    'title': 'AddColumnNode',
                    'user_input': '',
                }
            ],
        ),
    ],
)
def test_node_disable(session_id, toggle_request_body, expected):
    _ = session(session_id)
    _ = u.submit_loadNode({'session_id': session_id, 'parquet': {'path': TEST_STATE.path}})
    add_some_columns(session_id)

    res = requests.post('http://localhost:4444/rpc/node/toggleNode', json=toggle_request_body)

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
                    'prev_node_id': TEST_STATE.root_node_id,
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': False,
                    'title': 'AddColumnNode',
                    'user_input': '',
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
                    'prev_node_id': u.to_node_id(5),
                    'invalid_state': {
                        'active': True,
                        'error_msg': "UNRESOLVED_COLUMN.WITH_SUGGESTION with {'objectName': '`x`', 'proposal': '`tld`, `dnssec`, `domain`, `registrar`, `created_at`'} in node: node_0001",  # noqa
                    },
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
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
                    'prev_node_id': u.to_node_id(1),
                    'invalid_state': {
                        'active': True,
                        'error_msg': "UNRESOLVED_COLUMN.WITH_SUGGESTION with {'objectName': '`x`', 'proposal': '`tld`, `dnssec`, `domain`, `registrar`, `created_at`'} in node: node_0001",  # noqa
                    },
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
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
                    'prev_node_id': TEST_STATE.root_node_id,
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
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
                    'prev_node_id': u.to_node_id(5),
                    'invalid_state': {
                        'active': False,
                        'error_msg': '',
                    },
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
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
                    'prev_node_id': u.to_node_id(1),
                    'invalid_state': {
                        'active': False,
                        'error_msg': '',
                    },
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
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

    res = requests.post('http://localhost:4444/rpc/node/toggleNode', json=toggle_request_body)
    assert res.status_code == 200
    for a, b in zip(res.json(), expected_excluded, strict=True):
        assert json.dumps(a) == json.dumps(b)

    toggle_request_body['toggle'] = True
    res = requests.post('http://localhost:4444/rpc/node/toggleNode', json=toggle_request_body)
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
                    'columns': [{'name': 'name', 'dtype': 'string'}, {'name': 'session_id', 'dtype': 'long'}],
                    'session_id': u.to_session_id(9),
                    'node_id': TEST_STATE.root_node_id,
                    'prev_node_id': TEST_STATE.root_node_id,
                    'invalid_state': {
                        'active': False,
                        'error_msg': '',
                    },
                    'active': True,
                    'title': 'LoadNode',
                    'user_input': '',
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
                    'prev_node_id': TEST_STATE.root_node_id,
                    'invalid_state': {
                        'active': True,
                        'error_msg': "UNRESOLVED_COLUMN.WITH_SUGGESTION with {'objectName': '`domain`', 'proposal': '`name`, `session_id`'} in node: node_0001",  # noqa
                    },
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
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
                    'prev_node_id': u.to_node_id(1),
                    'invalid_state': {
                        'active': True,
                        'error_msg': "UNRESOLVED_COLUMN.WITH_SUGGESTION with {'objectName': '`domain`', 'proposal': '`name`, `session_id`'} in node: node_0001",  # noqa
                    },
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
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
                    'prev_node_id': TEST_STATE.root_node_id,
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                    'title': 'LoadNode',
                    'user_input': '',
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
                    'prev_node_id': TEST_STATE.root_node_id,
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
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
                    'prev_node_id': u.to_node_id(1),
                    'invalid_state': {'active': False, 'error_msg': ''},
                    'active': True,
                    'title': 'AddColumnNode',
                    'user_input': '',
                },
            ],
        ),
    ],
)
def test_input_path_replace(session_id, path_replace_request_body, expected):
    _ = session(session_id)
    _ = u.submit_loadNode({'session_id': session_id, 'parquet': {'path': TEST_STATE.path}})
    add_some_columns(session_id)

    res = requests.post('http://localhost:4444/rpc/node/submitLoadDatasetNode', json=path_replace_request_body)
    assert res.status_code == 200

    for a, b in zip(res.json(), expected, strict=True):
        assert json.dumps(a) == json.dumps(b)


@pytest.mark.parametrize(
    'session_requests, expected',
    [
        (
            [{'session_id': u.to_session_id(100)}],
            [
                {
                    'nodes': [
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
                            'session_id': '',
                            'node_id': '0000-0000-0000',
                            'prev_node_id': '0000-0000-0000',
                            'invalid_state': {'active': False, 'error_msg': ''},
                            'active': True,
                            'title': 'LoadNode',
                            'user_input': '{"path": ' + f'"{CURRENT_DIR}/../../data/domains_small.parquet' + '"}',
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
                            'session_id': '',
                            'node_id': 'node_0001',
                            'prev_node_id': '0000-0000-0000',
                            'invalid_state': {'active': False, 'error_msg': ''},
                            'active': True,
                            'title': 'AddColumnNode',
                            'user_input': '[{"expression": {"methodName": "upper", "compiled": "upper(domain) as a2"}}]',
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
                            'session_id': '',
                            'node_id': 'node_0002',
                            'prev_node_id': 'node_0001',
                            'invalid_state': {'active': False, 'error_msg': ''},
                            'active': True,
                            'title': 'AddColumnNode',
                            'user_input': '[{"expression": {"methodName": "upper", "compiled": "upper(tld) as b2"}}]',
                        },
                    ],
                    'session_id': 'session_0100',
                    'name': 'random_name',
                }
            ],
        ),
        (
            [{'session_id': u.to_session_id(101)}, {'session_id': u.to_session_id(102)}],
            [
                {
                    'nodes': [
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
                            'session_id': '',
                            'node_id': '0000-0000-0000',
                            'prev_node_id': '0000-0000-0000',
                            'invalid_state': {'active': False, 'error_msg': ''},
                            'active': True,
                            'title': 'LoadNode',
                            'user_input': '{"path": ' + f'"{CURRENT_DIR}/../../data/domains_small.parquet' + '"}',
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
                            'session_id': '',
                            'node_id': 'node_0001',
                            'prev_node_id': '0000-0000-0000',
                            'invalid_state': {'active': False, 'error_msg': ''},
                            'active': True,
                            'title': 'AddColumnNode',
                            'user_input': '[{"expression": {"methodName": "upper", "compiled": "upper(domain) as a2"}}]',
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
                            'session_id': '',
                            'node_id': 'node_0002',
                            'prev_node_id': 'node_0001',
                            'invalid_state': {'active': False, 'error_msg': ''},
                            'active': True,
                            'title': 'AddColumnNode',
                            'user_input': '[{"expression": {"methodName": "upper", "compiled": "upper(tld) as b2"}}]',
                        },
                    ],
                    'session_id': 'session_0101',
                    'name': 'random_name',
                },
                {
                    'nodes': [
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
                            'session_id': '',
                            'node_id': '0000-0000-0000',
                            'prev_node_id': '0000-0000-0000',
                            'invalid_state': {'active': False, 'error_msg': ''},
                            'active': True,
                            'title': 'LoadNode',
                            'user_input': '{"path": ' + f'"{CURRENT_DIR}/../../data/domains_small.parquet' + '"}',
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
                            'session_id': '',
                            'node_id': 'node_0001',
                            'prev_node_id': '0000-0000-0000',
                            'invalid_state': {'active': False, 'error_msg': ''},
                            'active': True,
                            'title': 'AddColumnNode',
                            'user_input': '[{"expression": {"methodName": "upper", "compiled": "upper(domain) as a2"}}]',
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
                            'session_id': '',
                            'node_id': 'node_0002',
                            'prev_node_id': 'node_0001',
                            'invalid_state': {'active': False, 'error_msg': ''},
                            'active': True,
                            'title': 'AddColumnNode',
                            'user_input': '[{"expression": {"methodName": "upper", "compiled": "upper(tld) as b2"}}]',
                        },
                    ],
                    'session_id': 'session_0102',
                    'name': 'random_name',
                },
            ],
        ),
    ],
)
def test_load_sessions(session_requests, expected):
    for session_request in session_requests:
        _ = session(session_request['session_id'])
        _ = u.submit_loadNode({'session_id': session_request['session_id'], 'parquet': {'path': TEST_STATE.path}})
        add_some_columns(session_request['session_id'])

    res = requests.get('http://localhost:4444/rpc/session/sessions')
    assert res.status_code == 200

    res_json = list(filter(lambda x: x['session_id'] in [req['session_id'] for req in session_requests], res.json()))

    print(res_json)
    print()
    print(expected)

    for a, b in zip(res_json, expected, strict=True):
        assert json.dumps(a) == json.dumps(b)
