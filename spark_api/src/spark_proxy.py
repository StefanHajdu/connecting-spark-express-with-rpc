from collections.abc import Iterable

import sparkapi_pb2
from sparkapi_pb2_grpc import SparkApiServicer

from Client import ClientSession
from PipelinePlan import SessionPlanner
from spark_session_init import clientSessionTable, spark


class SparkApiServicer(SparkApiServicer):
    def createSession(self, req: sparkapi_pb2.NewSessionRequest, unused_context) -> sparkapi_pb2.NewSessionResponse:
        clientSessionTable.add(req.id, ClientSession(req.id))

        return sparkapi_pb2.NewSessionResponse(
            id=req.id,
            msg=f'Session {req.id} created.',
        )

    def create_loadDatasetNode(self, req: sparkapi_pb2.LoadDatasetNodeRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)

        node = session.add_node(node_class='LoadNode', session_id=session.id, path=req.df_path, data_type=req.df_type)

        session.plan = SessionPlanner(req.session_id, node)
        return sparkapi_pb2.SparkTransformResponse(session_id=req.session_id, msg=f'Dataset {req.df_path} loaded.')

    def create_loadFromSessionNode(
        self, req: sparkapi_pb2.LoadFromSessionNodeRequest, unused_context
    ) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)

        parent_session = clientSessionTable.get_session(req.input_session_id)
        node = session.add_node(node_class='LoadFromSessionNode', session_id=session.id, parent_session_plan=parent_session.plan)
        parent_session.add_child_session(session)

        session.plan = SessionPlanner(req.session_id, node)
        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Dataframe from input session {req.input_session_id} reused input.',
        )

    def create_FilterNode(self, req: sparkapi_pb2.FilterNodeRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        node = session.add_node(
            node_class='FilterNode',
            session_id=session.id,
            node_id=req.node_id,
            prev_node_id=req.prev_node_id,
            expressions=list(req.expressions),
            matching=req.matching,
            prev_df=session.plan.get_node_by_id(req.prev_node_id).df,
        )
        session.plan.add_node(spark, node)
        session.notify_transformation_change()

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Node: {req.node_id} added',
        )

    def create_NewColumnNode(self, req: sparkapi_pb2.NewColumnNodeRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        node = session.add_node(
            node_class='NewColumnNode',
            session_id=session.id,
            node_id=req.node_id,
            prev_node_id=req.prev_node_id,
            expressions=list(req.expressions),
            prev_df=session.plan.get_node_by_id(req.prev_node_id).df,
        )
        session.plan.add_node(spark, node)
        session.notify_transformation_change()

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Node: {req.node_id} added',
        )

    def create_JoinNode(self, req: sparkapi_pb2.JoinNodeRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        node = session.add_node(
            node_class='JoinNode',
            session_id=session.id,
            node_id=req.node_id,
            prev_node_id=req.prev_node_id,
            input_type=req.input_type,
            input_pointer=req.input_pointer,
            prev_df=session.plan.get_node_by_id(req.prev_node_id).df,
        )
        session.plan.add_node(spark, node)
        session.notify_transformation_change()

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Node: {req.node_id} added',
        )

    def create_TableNode(self, req: sparkapi_pb2.AddNodeRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        node = session.add_node(node_class='TableNode', session_id=session.id, node_id=req.node_id, prev_node_id=req.prev_node_id)
        session.plan.add_visualization_node(spark, node)

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Node: {req.node_id} added',
        )

    def edit_FilterNode(self, req: sparkapi_pb2.FilterNodeRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        session.edit_node(req.node_id, expressions=list(req.expressions), matching=req.matching)

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Node: {req.node_id} edited',
        )

    def edit_NewColumnNode(self, req: sparkapi_pb2.NewColumnNodeRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        session.edit_node(req.node_id, expressions=list(req.expressions))

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Node: {req.node_id} edited',
        )

    def edit_JoinNode(self, req: sparkapi_pb2.JoinNodeRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        session.edit_node(
            req.node_id,
            join_relation=req.join_relation,
            columns_to_keep=list(req.columns_to_keep),
            columns_to_add=list(req.columns_to_add),
            prefix_for_added_columns=req.prefix_for_added_columns,
            join_criteria=list(req.join_criteria),
            criteria_matching=req.criteria_matching,
        )

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Node: {req.node_id} edited',
        )

    def removeNode(self, req: sparkapi_pb2.NodeRemovalRequest, unused_context) -> sparkapi_pb2.PysparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        session.remove_node(req.node_id)

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Node: {req.node_id} removed',
        )

    def rebuildSession(self, req: sparkapi_pb2.RebuildRequest, unused_context) -> sparkapi_pb2.PysparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        session.rebuild()

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Session: {req.session_id} rebuild',
        )

    def summarizeDataset(self, req: sparkapi_pb2.SummarizeDatasetRequest, unused_context) -> sparkapi_pb2.SparkActionlResponse:
        session = clientSessionTable.get_session(req.session_id)
        summary = session.summarize(req.node_id)

        return sparkapi_pb2.SparkActionlResponse(
            session_id=req.session_id,
            msg=f'Node {req.node_id} summarized',
            columns=summary['columns'],
            count=summary['count'],
            schema=summary['schema'],
        )

    def previewDataset(self, req: sparkapi_pb2.PreviewDatasetRequest, unused_context) -> Iterable[sparkapi_pb2.RowStreamResponse]:
        session = clientSessionTable.get_session(req.session_id)
        row_stream = session.preview(req.node_id, req.limit)

        for row in row_stream:
            yield sparkapi_pb2.RowStreamResponse(row_json=row)

    def getSessionStatus(self, req: sparkapi_pb2.SessionStatusRequest, unused_context) -> sparkapi_pb2.StatusResponse:
        session = clientSessionTable.get_session(req.session_id)

        return sparkapi_pb2.StatusResponse(session_id=req.session_id, **session.get_session_status())
