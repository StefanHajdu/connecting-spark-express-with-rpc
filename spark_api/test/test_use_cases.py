import json
import os
import uuid

import pytest
from exceptions import NodeMissingException
from state import TestState

import utils as u

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
NODE_MISSING_EXCEPTION = NodeMissingException()
TEST_STATE = TestState()


def test_01_submit_loadNode_and_summarize():
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    _ = u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})
    df_meta = u.summarize(session_id=session_0, node_id=TEST_STATE.root_node_id)
    assert df_meta['count'] == TEST_STATE.total_rows


@pytest.mark.skip(reason='Test not implemented')
def test_02_submit_loadFromSessionNode():
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    _ = u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})
    node_1 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'expressions': ["tld = '.com'"],
            'matching': '',
        }
    )
    df_session_0 = u.summarize(session_id=session_0, node_id=node_1)

    session_1 = u.create_session(session_id=u.to_session_id(1))
    u.submit_loadFromSessionNode(session_id=session_1, input_session_id=session_0)

    df_session_1 = u.summarize(session_id=session_1, node_id=TEST_STATE.root_node_id)
    assert df_session_0['count'] == df_session_1['count']


def test_03_filter():
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})
    node_1 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'expressions': ["tld = 'com'"],
            'matching': '',
        }
    )
    df_session_0 = u.summarize(session_id=session_0, node_id=node_1)
    node_2 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_2)
    node_3 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(3),
            'prev_node_id': node_2,
            'expressions': ["registrar = 'GoDaddy.com, LLC'"],
            'matching': '',
        }
    )
    df_session_2 = u.summarize(session_id=session_0, node_id=node_3)
    assert df_session_0['count'] > df_session_1['count']
    assert df_session_1['count'] > df_session_2['count']


@pytest.mark.skip(reason='Test not implemented')
def test_04_1_parent_session_changed():
    # session 0
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})
    node_01 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'expressions': ["tld = 'com'", "tld = 'org'"],
            'matching': 'or',
        }
    )
    node_02 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_01,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_01 = u.summarize(session_id=session_0, node_id=node_02)

    # session 1
    session_1 = u.create_session(session_id=u.to_session_id(1))
    u.submit_loadFromSessionNode(session_id=session_1, input_session_id=session_0)

    df_session_11 = u.summarize(session_id=session_1, node_id=TEST_STATE.root_node_id)
    assert df_session_01['count'] == df_session_11['count']
    node_11 = u.submit_filterNode(
        **{
            'session_id': session_1,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'expressions': ["registrar = 'NameCheap, Inc.'"],
            'matching': '',
        }
    )
    df_session_12 = u.summarize(session_id=session_1, node_id=node_11)

    # session 0
    node_03 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(3),
            'prev_node_id': node_02,
            'expressions': ["tld = '.com'"],
            'matching': '',
        }
    )
    assert u.get_rebuild_status(session_1)
    df_session_02 = u.summarize(session_id=session_0, node_id=node_03)
    assert df_session_02['count'] < df_session_01['count'] and u.get_rebuild_status(session_1)

    # session 1
    u.rebuild_session(session_1)
    assert not u.get_rebuild_status(session_1)
    df_session_13 = u.summarize(session_id=session_1, node_id=node_11)
    assert df_session_13['count'] < df_session_12['count']


@pytest.mark.skip(reason='Test not implemented')
def test_04_2_parent_session_changed_multi_level():
    # session 0
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})
    node_01 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'previous_node_id': TEST_STATE.root_node_id,
            'expressions': ["tld = 'com'", "tld = 'org'"],
            'matching': 'or',
        }
    )
    df_session_01 = u.summarize(session_id=session_0, node_id=node_01)

    # session 1
    session_1 = u.create_session(session_id=u.to_session_id(1))
    u.submit_loadFromSessionNode(session_id=session_1, input_session_id=session_0)
    node_11 = u.submit_filterNode(
        **{
            'session_id': session_1,
            'node_id': u.to_node_id(1),
            'previous_node_id': TEST_STATE.root_node_id,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_11 = u.summarize(session_id=session_1, node_id=node_11)

    # session 2
    session_2 = u.create_session(session_id=u.to_session_id(2))
    u.submit_loadFromSessionNode(session_id=session_2, input_session_id=session_1)
    node_21 = u.submit_filterNode(
        **{
            'session_id': session_2,
            'node_id': u.to_node_id(1),
            'previous_node_id': TEST_STATE.root_node_id,
            'expressions': ["registrar = 'GoDaddy.com, LLC'"],
            'matching': '',
        }
    )
    df_session_21 = u.summarize(session_id=session_2, node_id=node_21)

    # session 0
    node_11 = u.submit_filterNode(**{'session_id': session_0, 'node_id': node_11, 'expressions': ["tld = '.com'"], 'matching': ''})

    # rebuilds
    assert u.get_rebuild_status(session_1)
    assert not u.get_rebuild_status(session_2)

    u.rebuild_session(session_1)
    assert not u.get_rebuild_status(session_1)
    assert u.get_rebuild_status(session_2)

    u.rebuild_session(session_2)
    assert not u.get_rebuild_status(session_1)
    assert not u.get_rebuild_status(session_2)

    # summarize
    df_session_02 = u.summarize(session_id=session_0, node_id=node_11)
    df_session_12 = u.summarize(session_id=session_1, node_id=node_11)
    df_session_22 = u.summarize(session_id=session_2, node_id=node_21)

    assert df_session_02['count'] < df_session_01['count']
    assert df_session_12['count'] < df_session_11['count']
    assert df_session_22['count'] < df_session_21['count']


def test_05_append_sql():
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})
    node_1 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'expressions': ["tld = 'com'", "tld = 'org'"],
            'matching': 'or',
        }
    )
    node_2 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_2)

    node_3 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(3),
            'prev_node_id': node_2,
            'expressions': ["tld = '.com'"],
            'matching': '',
        }
    )
    df_session_2 = u.summarize(session_id=session_0, node_id=node_3)
    assert df_session_2['count'] < df_session_1['count']


def test_05_submit_filterNode_before_summarize():
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})
    node_1 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    node_2 = u.submit_newColumnNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [{'expression': 'length(registrar)', 'col_name': 'registrar_len'}],
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_2)

    # add before cached
    _ = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(3),
            'prev_node_id': node_1,
            'expressions': ["tld = '.com'"],
            'matching': '',
        }
    )
    df_session_2 = u.summarize(session_id=session_0, node_id=node_2)
    assert df_session_2['count'] < df_session_1['count']


def test_06_unordered_summarize():
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})
    node_1 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'expressions': ["tld = 'com'"],
            'matching': '',
        }
    )
    node_2 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    node_3 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(3),
            'prev_node_id': node_2,
            'expressions': ["registrar = 'GoDaddy.com, LLC'"],
            'matching': '',
        }
    )

    df_session_3 = u.summarize(session_id=session_0, node_id=node_3)
    df_session_1 = u.summarize(session_id=session_0, node_id=node_1)
    df_session_2 = u.summarize(session_id=session_0, node_id=node_2)
    assert df_session_1['count'] > df_session_2['count']
    assert df_session_2['count'] > df_session_3['count']


def test_07_submit_filterNode_after_summarize():
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})
    node_1 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'expressions': ["tld = 'com'", "tld = 'org'"],
            'matching': 'or',
        }
    )
    node_2 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_1)

    node_2 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': node_2,
            'prev_node_id': node_1,
            'expressions': ["registrar = 'GoDaddy.com, LLC'"],
            'matching': '',
        }
    )
    df_session_2 = u.summarize(session_id=session_0, node_id=node_2)
    assert df_session_1['count'] > df_session_2['count']


def test_07_submit_filterNode_before_summarize():
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})
    node_1 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'expressions': ["tld = 'com'", "tld = 'org'"],
            'matching': 'or',
        }
    )
    node_2 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_1)

    node_2 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': node_1,
            'prev_node_id': TEST_STATE.root_node_id,
            'expressions': ["tld = '.com'"],
            'matching': '',
        }
    )
    df_session_2 = u.summarize(session_id=session_0, node_id=node_2)
    assert df_session_1['count'] > df_session_2['count']


def test_08_removeNode_after_summarize():
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})
    node_1 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'expressions': ["tld = '.com'"],
            'matching': '',
        }
    )
    node_2 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    u.removeNode(
        **{
            'session_id': session_0,
            'node_id': node_1,
        }
    )

    u.removeNode(
        **{
            'session_id': session_0,
            'node_id': node_2,
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_2)
    assert NODE_MISSING_EXCEPTION.__str__() in df_session_1['error']['message']
    df_session_2 = u.summarize(session_id=session_0, node_id=TEST_STATE.root_node_id)
    assert df_session_2['count'] == TEST_STATE.total_rows


def test_08_removeNode_before_summarize():
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})
    node_1 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'expressions': ["tld = '.com'"],
            'matching': '',
        }
    )
    node_2 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_2)

    u.removeNode(
        **{
            'session_id': session_0,
            'node_id': node_1,
        }
    )
    df_session_2 = u.summarize(session_id=session_0, node_id=node_2)
    assert df_session_1['count'] < df_session_2['count']

    u.removeNode(
        **{
            'session_id': session_0,
            'node_id': node_2,
        }
    )
    df_session_3 = u.summarize(session_id=session_0, node_id=node_2)
    assert NODE_MISSING_EXCEPTION.__str__() in df_session_3['error']['message']
    df_session_4 = u.summarize(session_id=session_0, node_id=TEST_STATE.root_node_id)
    assert df_session_4['count'] == TEST_STATE.total_rows


def test_12_toggle():
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})
    df_session_0 = u.summarize(session_id=session_0, node_id=TEST_STATE.root_node_id)

    node_1 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'expressions': ["tld = '.com'"],
            'matching': '',
        }
    )
    node_2 = u.submit_filterNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_2)

    u.toggleNode(**{'session_id': session_0, 'node_id': node_1, 'toggle': False})
    u.toggleNode(**{'session_id': session_0, 'node_id': node_2, 'toggle': False})

    res_all_disabled = u.summarize(session_id=session_0, node_id=node_2)
    assert df_session_0['count'] == res_all_disabled['count']

    u.toggleNode(**{'session_id': session_0, 'node_id': node_2, 'toggle': True})
    df_session_3 = u.summarize(session_id=session_0, node_id=node_2)
    assert df_session_3['count'] > df_session_1['count']

    u.toggleNode(**{'session_id': session_0, 'node_id': node_1, 'toggle': True})
    df_session_4 = u.summarize(session_id=session_0, node_id=node_2)
    assert df_session_4['count'] == df_session_1['count']


@pytest.mark.parametrize(
    'filter_function',
    [
        # text filtering
        {'case': {'expressions': ["contains(domain, 'club')"], 'matching': ''}, 'correct': 2475},
        {
            'case': {
                'expressions': ["ilike(registrar, 'G_Daddy.com, LLC')"],
                'matching': '',
            },
            'correct': 85127,
        },
        {
            'case': {
                'expressions': ["ilike(registrar, 'GoDaddy.com, LLC')"],
                'matching': '',
            },
            'correct': 85127,
        },
        {
            'case': {
                'expressions': ["ilike(registrar, 'GoDaddy.%, LLC')"],
                'matching': '',
            },
            'correct': 85127,
        },
        {'case': {'expressions': ["ilike(registrar, '成%维数码科技有限公司')"], 'matching': ''}, 'correct': 340},
        {
            'case': {
                'expressions': ["rlike(domain, '(https?:\/\/)?(www\.)?[a-z0-9-]+\.(com|org)(\.[a-z]{{2,3}})?')"],
                'matching': '',
            },
            'correct': 301352,
        },
        {'case': {'expressions': ["startswith(registrar, 'GoDaddy')"], 'matching': ''}, 'correct': 93668},
        {'case': {'expressions': ["endswith(registrar, 'com')"], 'matching': ''}, 'correct': 19551},
        {'case': {'expressions': ['length(registrar) < 10'], 'matching': ''}, 'correct': 153053},
        # numerical filtering
        {'case': {'expressions': ['numerical_col == 1'], 'matching': ''}, 'correct': 499_999},
        {'case': {'expressions': ['numerical_col > 2'], 'matching': ''}, 'correct': 0},
        {'case': {'expressions': ['numerical_col < -1'], 'matching': ''}, 'correct': 0},
        {'case': {'expressions': ['numerical_col >= 2'], 'matching': ''}, 'correct': 0},
        {'case': {'expressions': ['numerical_col <= -1'], 'matching': ''}, 'correct': 0},
        {'case': {'expressions': ['numerical_col between -1 and 2'], 'matching': ''}, 'correct': 499_999},
        # date filtering
        {'case': {'expressions': ['date_col == current_date()'], 'matching': ''}, 'correct': 0},
        {'case': {'expressions': ['date_col > current_date()'], 'matching': ''}, 'correct': 0},
        {'case': {'expressions': ['date_col < current_date()'], 'matching': ''}, 'correct': 375585},
        {'case': {'expressions': ['date_col >= current_date()'], 'matching': ''}, 'correct': 0},
        {'case': {'expressions': ['date_col <= current_date()'], 'matching': ''}, 'correct': 375585},
        {
            'case': {'expressions': ['date_col between to_date("01-01-1970", "MM-dd-yyyy") and current_date()'], 'matching': ''},
            'correct': 375585,
        },
        # array filtering
        {'case': {'expressions': ["array_contains(array_col, 'thomas-ds.com')"], 'matching': ''}, 'correct': 1},
        {
            'case': {'expressions': ["arrays_overlap(array_col, array('thomas-ds.com', 'Squarespace Domains LLC'))"], 'matching': ''},
            'correct': 12510,
        },
        # null filtering
        {'case': {'expressions': ['isnull(created_at)'], 'matching': ''}, 'correct': 124414},
        {'case': {'expressions': ['isnotnull(created_at)'], 'matching': ''}, 'correct': 375585},
    ],
)
def test_13_text_filter(filter_function):
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})
    # add numerical col
    node_1 = u.submit_newColumnNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'user_input': [
                {
                    'expression': {
                        'compiled': '1 as numerical_col',
                        'method_name': 'constant',
                        'params': [],
                    }
                }
            ],
        }
    )
    # add array col
    node_2 = u.submit_newColumnNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'user_input': [
                {
                    'expression': {
                        'compiled': 'array(domain, registrar) as array_col',
                        'method_name': 'array',
                        'params': [],
                    }
                }
            ],
        }
    )
    # add date col
    node_3 = u.submit_newColumnNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(3),
            'prev_node_id': node_2,
            'user_input': [
                {
                    'expression': {
                        'compiled': 'to_date(created_at) as date_col',
                        'method_name': 'to_date',
                        'params': [],
                    }
                }
            ],
        }
    )
    node_4 = u.submit_filterNode(
        **{
            **{'session_id': session_0, 'node_id': u.to_node_id(4), 'prev_node_id': node_3},
            **filter_function['case'],
        }
    )

    df_session = u.summarize(session_id=session_0, node_id=node_4)
    if df_session['count'] != filter_function['correct']:
        print(filter_function['case'])
    assert df_session['count'] == filter_function['correct']


@pytest.mark.parametrize(
    'math_numerical_function',
    [
        {'expression': {'compiled': 'abs(numerical_col) as res', 'method_name': ''}},
        {'expression': {'compiled': 'cbrt(numerical_col) as res', 'method_name': ''}},
        {'expression': {'compiled': 'ceil(numerical_col) as res', 'method_name': ''}},
        {'expression': {'compiled': 'cos(numerical_col) as res', 'method_name': ''}},
        {'expression': {'compiled': 'exp(numerical_col) as res', 'method_name': ''}},
        {'expression': {'compiled': 'factorial(numerical_col) as res', 'method_name': ''}},
        {'expression': {'compiled': 'floor(numerical_col) as res', 'method_name': ''}},
        {'expression': {'compiled': 'ln(numerical_col) as res', 'method_name': ''}},
        {'expression': {'compiled': 'log(numerical_col) as res', 'method_name': ''}},
        {'expression': {'compiled': 'pow(numerical_col, 2) as res', 'method_name': ''}},
        {'expression': {'compiled': 'rand(42) as res', 'method_name': ''}},
        {'expression': {'compiled': 'round(numerical_col) as res', 'method_name': ''}},
        {'expression': {'compiled': 'sin(numerical_col) as res', 'method_name': ''}},
        {'expression': {'compiled': 'sqrt(numerical_col) as res', 'method_name': ''}},
        {'expression': {'compiled': 'tan(numerical_col) as res', 'method_name': ''}},
    ],
)
def test_14_addColumn_math_numerical_functions(math_numerical_function):
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})
    node_1 = u.submit_newColumnNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'user_input': [
                {
                    'expression': {
                        'compiled': '1 as numerical_col',
                        'method_name': 'constant',
                        'params': [],
                    }
                }
            ],
        }
    )
    node_2 = u.submit_newColumnNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'user_input': [math_numerical_function],
        }
    )
    df_session = u.summarize(session_id=session_0, node_id=node_2)

    cols = json.loads(df_session['columns'])
    assert 'res' in cols


@pytest.mark.parametrize(
    'string_function',
    [
        {'expression': {'compiled': 'concat(domain, registrar) as res', 'method_name': ''}},
        {'expression': {'compiled': "concat_ws('-', domain, registrar) as res", 'method_name': ''}},
        {'expression': {'compiled': 'length(domain) as res', 'method_name': ''}},
        {'expression': {'compiled': 'levenshtein(domain, registrar) as res', 'method_name': ''}},
        {'expression': {'compiled': 'lower(registrar) as res', 'method_name': ''}},
        {'expression': {'compiled': "lpad(domain, 30, '#') as res", 'method_name': ''}},
        {'expression': {'compiled': 'ltrim(domain) as res', 'method_name': ''}},
        {
            'expression': {
                'compiled': "regexp_extract(domain, '(\d+)-(\d+)') as res",
                'method_name': '',
                'params': [],
            }
        },
        {
            'expression': {
                'compiled': "regexp_replace(domain, '(\d+)', '--') as res",
                'method_name': '',
                'params': [],
            }
        },
        {'expression': {'compiled': 'reverse(domain) as res', 'method_name': ''}},
        {'expression': {'compiled': "rpad(domain, 30, '#') as res", 'method_name': ''}},
        {'expression': {'compiled': 'rtrim(domain) as res', 'method_name': ''}},
        {'expression': {'compiled': "split(domain, '[a]', 2) as res", 'method_name': ''}},
        {'expression': {'compiled': 'substring(domain, 1, 2) as res', 'method_name': ''}},
        {'expression': {'compiled': 'trim(registrar) as res', 'method_name': ''}},
        {'expression': {'compiled': 'upper(domain) as res', 'method_name': ''}},
    ],
)
def test_15_addColumn_string_functions(string_function):
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})
    node_1 = u.submit_newColumnNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'user_input': [string_function],
        }
    )
    df_session = u.summarize(session_id=session_0, node_id=node_1)

    cols = json.loads(df_session['columns'])
    assert 'res' in cols


@pytest.mark.parametrize(
    'array_function',
    [
        {
            'expression': {
                'compiled': "array_contains(array_col, 'nasmo.se') as res",
                'method_name': '',
                'params': [],
            }
        },
        {'expression': {'compiled': 'element_at(array_col, 1) as res', 'method_name': ''}},
        {'expression': {'compiled': 'array_size(array_col) as res', 'method_name': ''}},
        {'expression': {'compiled': "array_join(array_col, '---') as res", 'method_name': ''}},
        {'expression': {'compiled': 'array_sort(array_col) as res', 'method_name': ''}},
    ],
)
def test_16_addColumn_array_functions(array_function):
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})

    node_1 = u.submit_newColumnNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'user_input': [
                {
                    'expression': {
                        'compiled': 'array(domain, registrar) as array_col',
                        'method_name': '',
                        'params': [],
                    }
                },
            ],
        }
    )

    node_2 = u.submit_newColumnNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'user_input': [array_function],
        }
    )
    df_session = u.summarize(session_id=session_0, node_id=node_2)

    cols = json.loads(df_session['columns'])
    assert 'res' in cols


@pytest.mark.parametrize(
    'date_function',
    [
        {'expression': {'compiled': 'add_months(date_col_1, 10) as res', 'method_name': ''}},
        {'expression': {'compiled': 'date_add(date_col_1, 10) as res', 'method_name': ''}},
        {
            'expression': {
                'compiled': "date_format(date_col_1, 'MM/dd/yyy') as res",
                'method_name': '',
                'params': [],
            }
        },
        {'expression': {'compiled': 'date_sub(date_col_1, 10) as res', 'method_name': ''}},
        {'expression': {'compiled': "date_trunc('year', date_col_1) as res", 'method_name': ''}},
        {'expression': {'compiled': 'date_diff(date_col_1, date_col_2) as res', 'method_name': ''}},
        {'expression': {'compiled': 'dayofmonth(date_col_1) as res', 'method_name': ''}},
        {'expression': {'compiled': 'dayofweek(date_col_1) as res', 'method_name': ''}},
        {'expression': {'compiled': 'dayofyear(date_col_1) as res', 'method_name': ''}},
        {
            'expression': {
                'compiled': "from_utc_timestamp(date_col_1, 'PST') as res",
                'method_name': '',
                'params': [],
            }
        },
        {'expression': {'compiled': 'hour(date_col_1) as res', 'method_name': ''}},
        {'expression': {'compiled': 'last_day(date_col_1) as res', 'method_name': ''}},
        {'expression': {'compiled': 'minute(date_col_1) as res', 'method_name': ''}},
        {'expression': {'compiled': 'month(date_col_1) as res', 'method_name': ''}},
        {
            'expression': {
                'compiled': 'months_between(date_col_1, date_col_2) as res',
                'method_name': '',
                'params': [],
            }
        },
        {'expression': {'compiled': 'quarter(date_col_1) as res', 'method_name': ''}},
        {'expression': {'compiled': 'second(date_col_1) as res', 'method_name': ''}},
        {'expression': {'compiled': 'to_unix_timestamp(created_at) as res', 'method_name': ''}},
        {
            'expression': {
                'compiled': "to_utc_timestamp(created_at, 'JST') as res",
                'method_name': '',
                'params': [],
            }
        },
        {'expression': {'compiled': 'weekofyear(date_col_1) as res', 'method_name': ''}},
        {'expression': {'compiled': 'year(date_col_1) as res', 'method_name': ''}},
    ],
)
def test_17_addColumn_date_functions(date_function):
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})

    node_1 = u.submit_newColumnNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'user_input': [
                {
                    'expression': {
                        'compiled': 'current_date() as date_col_1',
                        'method_name': '',
                        'params': [],
                    }
                },
                {
                    'expression': {
                        'compiled': 'current_timestamp() as date_col_2',
                        'method_name': '',
                        'params': [],
                    }
                },
                {
                    'expression': {
                        'compiled': 'unix_timestamp() as date_col_3',
                        'method_name': '',
                        'params': [],
                    }
                },
            ],
        }
    )

    node_2 = u.submit_newColumnNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'user_input': [date_function],
        }
    )
    df_session = u.summarize(session_id=session_0, node_id=node_2)

    cols = json.loads(df_session['columns'])
    assert 'res' in cols


@pytest.mark.parametrize(
    'misc_function',
    [
        {'expression': {'compiled': 'coalesce(domain, registrar) as res', 'method_name': ''}},
        {'expression': {'compiled': 'greatest(domain, registrar) as res', 'method_name': ''}},
        {'expression': {'compiled': 'hash(domain) as res', 'method_name': ''}},
        {'expression': {'compiled': 'isnull(domain) as res', 'method_name': ''}},
        {'expression': {'compiled': 'least(domain, registrar) as res', 'method_name': ''}},
        {'expression': {'compiled': 'md5(domain) as res', 'method_name': ''}},
        {'expression': {'compiled': 'monotonically_increasing_id() as res', 'method_name': ''}},
        {'expression': {'compiled': 'sha1(domain) as res', 'method_name': ''}},
        # {
        #     'expression': {
        #         'compiled': "from_json(from_json(js, 'MAP<STRING,STRING>') as res",
        #         'method_name': '',
        #         'params': [],
        #     }
        # },
    ],
)
def test_18_misc_functions(misc_function):
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'parquet': {'path': TEST_STATE.path}})

    node_2 = u.submit_newColumnNode(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': TEST_STATE.root_node_id,
            'user_input': [misc_function],
        }
    )
    df_session = u.summarize(session_id=session_0, node_id=node_2)

    cols = json.loads(df_session['columns'])
    assert 'res' in cols


@pytest.mark.parametrize(
    'join_relation',
    [
        {
            'case': {
                'join_relation': 'inner',
                'columns_to_keep': ['name', 'session_id'],
                'columns_to_add': ['name', 'session_id'],
                'prefix_for_added_columns': '_',
                'join_criteria': ['{df}.name == {other_df}.name'],
                'criteria_matching': '',
            },
            'correct_num_rows': 2,
        },
        {
            'case': {
                'join_relation': 'cross',
                'columns_to_keep': ['name', 'session_id'],
                'columns_to_add': ['name', 'session_id'],
                'prefix_for_added_columns': '_',
                'join_criteria': [],
                'criteria_matching': '',
            },
            'correct_num_rows': 16,
        },
        {
            'case': {
                'join_relation': 'full',
                'columns_to_keep': ['name', 'session_id'],
                'columns_to_add': ['name', 'session_id'],
                'prefix_for_added_columns': '_',
                'join_criteria': ['{df}.name == {other_df}.name'],
                'criteria_matching': '',
            },
            'correct_num_rows': 6,
        },
        {
            'case': {
                'join_relation': 'left',
                'columns_to_keep': ['name', 'session_id'],
                'columns_to_add': ['name', 'session_id'],
                'prefix_for_added_columns': '_',
                'join_criteria': ['{df}.name == {other_df}.name'],
                'criteria_matching': '',
            },
            'correct_num_rows': 4,
        },
        {
            'case': {
                'join_relation': 'right',
                'columns_to_keep': ['name', 'session_id'],
                'columns_to_add': ['name', 'session_id'],
                'prefix_for_added_columns': '_',
                'join_criteria': ['{df}.name == {other_df}.name'],
                'criteria_matching': '',
            },
            'correct_num_rows': 4,
        },
        {
            'case': {
                'join_relation': 'left semi',
                'columns_to_keep': ['name', 'session_id'],
                'columns_to_add': [],
                'prefix_for_added_columns': '',
                'join_criteria': ['{df}.name == {other_df}.name'],
                'criteria_matching': '',
            },
            'correct_num_rows': 2,
        },
        {
            'case': {
                'join_relation': 'left anti',
                'columns_to_keep': ['name', 'session_id'],
                'columns_to_add': [],
                'prefix_for_added_columns': '',
                'join_criteria': ['{df}.name == {other_df}.name'],
                'criteria_matching': '',
            },
            'correct_num_rows': 2,
        },
    ],
)
def test_19_join_relations(join_relation):
    session_0 = u.create_session(session_id=str(uuid.uuid4()))
    u.submit_loadNode({'session_id': session_0, 'json': {'multiline': True, 'path': f'{CURRENT_DIR}/../../data/df1.json'}})
    node_1 = u.submit_joinNode(
        **{
            'session_id': session_0,
            'node_id': 'n0001',
            'prev_node_id': TEST_STATE.root_node_id,
            'json': {'multiline': True, 'path': f'{CURRENT_DIR}/../../data/df2.json'},
            'joinParams': {},
        }
    )

    node_1 = u.submit_joinNode(
        **{
            **{
                'session_id': session_0,
                'node_id': 'n0001',
                'prev_node_id': TEST_STATE.root_node_id,
                'json': {'multiline': True, 'path': f'{CURRENT_DIR}/../../data/df2.json'},
                'joinParams': join_relation['case'],
            }
        }
    )

    df_session = u.summarize(session_id=session_0, node_id=node_1)

    assert set([join_relation['case']['prefix_for_added_columns'] + col for col in join_relation['case']['columns_to_add']]).issubset(
        set(json.loads(df_session['columns']))
    )
    assert df_session['count'] == join_relation['correct_num_rows']
