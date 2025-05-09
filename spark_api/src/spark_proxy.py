import time

import sparkapi_pb2
from sparkapi_pb2_grpc import SparkApiServicer

from Client import ClientSession
from PipelinePlan import SessionPlanner
from spark_session_init import clientSessionTable, spark


class SparkApiServicer(SparkApiServicer):
    def createSession(self, req: sparkapi_pb2.NewSessionRequest, unused_context) -> sparkapi_pb2.NewSessionResponse:
        clientSessionTable.add(req.id, ClientSession(req.id, req.name))

        return sparkapi_pb2.NewSessionResponse(
            session_id=req.id,
            msg=f'Session {req.id} created.',
        )

    # create node
    def submit_LoadDatasetNode(self, req: sparkapi_pb2.LoadDatasetNodeRequest, unused_context) -> sparkapi_pb2.SparkLoadFileResponse:
        session = clientSessionTable.get_session(req.session_id)

        node = session.submit_node(node_class='LoadNode', session_id=session.id, path=req.path)

        session.plan = SessionPlanner(req.session_id, node)
        return sparkapi_pb2.SparkLoadFileResponse(
            transformResponse=sparkapi_pb2.SparkTransformResponse(
                session_id=req.session_id,
                msg=f'LOADED: {req.path}.',
                columns=node.columns,
            ),
            size=node.input_size,
        )

    def submit_LoadFromSessionNode(
        self, req: sparkapi_pb2.LoadFromSessionNodeRequest, unused_context
    ) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)

        parent_session = clientSessionTable.get_session(req.input_session_id)
        node = session.submit_node(node_class='LoadFromSessionNode', session_id=session.id, parent_session_plan=parent_session.plan)
        parent_session.add_child_session(session)

        session.plan = SessionPlanner(req.session_id, node)
        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id, msg=f'Dataframe from input session {req.input_session_id} reused input.', columns=node.columns
        )

    def submit_FilterNode(self, req: sparkapi_pb2.FilterNodeRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        node = session.submit_node(
            node_class='FilterNode',
            session_id=session.id,
            node_id=req.node_id,
            prev_node_id=req.prev_node_id,
            expressions=list(req.expressions),
            matching=req.matching,
            prev_df=session.plan.get_node_by_id(req.prev_node_id).df,
        )
        session.plan.process_node(spark, node)
        session.notify_transformation_change()

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Node: {req.node_id} added',
            columns=node.columns,
        )

    def submit_NewColumnNode(self, req: sparkapi_pb2.NewColumnNodeRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        node = session.submit_node(
            node_class='NewColumnNode',
            session_id=session.id,
            node_id=req.node_id,
            prev_node_id=req.prev_node_id,
            expressions=list(req.expressions),
            prev_df=session.plan.get_node_by_id(req.prev_node_id).df,
        )
        session.plan.process_node(spark, node)
        session.notify_transformation_change()

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Node: {req.node_id} added',
            columns=node.columns,
        )

    def submit_JoinNode(self, req: sparkapi_pb2.JoinNodeRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        node = session.submit_node(
            node_class='JoinNode',
            session_id=session.id,
            node_id=req.node_id,
            prev_node_id=req.prev_node_id,
            input_type=req.input_type,
            input_pointer=req.input_pointer,
            joinParams=req.joinParams,
            prev_df=session.plan.get_node_by_id(req.prev_node_id).df,
        )
        session.plan.process_node(spark, node)
        session.notify_transformation_change()

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Node: {req.node_id} added',
            columns=node.columns,
        )

    def submit_TableNode(self, req: sparkapi_pb2.AddTableNodeRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        node = session.submit_node(
            node_class='TableNode',
            session_id=session.id,
            node_id=req.node_id,
            prev_node_id=req.prev_node_id,
            prev_df=session.plan.get_node_by_id(req.prev_node_id).df,
        )
        session.plan.process_node(spark, node)

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Node: {req.node_id} added',
            columns=node.columns,
        )

    def submit_HistogramNode(self, req: sparkapi_pb2.AddHistogramNodeRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        node = session.submit_node(
            node_class='HistogramNode',
            session_id=session.id,
            node_id=req.node_id,
            prev_node_id=req.prev_node_id,
            y_axis_col=req.y_axis_col,
            order_by=req.order_by,
            sort_by=req.sort_by,
            expression=req.expression,
            prev_df=session.plan.get_node_by_id(req.prev_node_id).df,
        )
        session.plan.process_node(spark, node)

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Node: {req.node_id} added',
            columns=node.columns,
        )

    # remove node
    def removeNode(self, req: sparkapi_pb2.NodeRemovalRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        node = session.plan.get_node_by_id(req.node_id)
        session.remove_node(node)

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Node: {req.node_id} removed',
        )

    # rebuild node
    def rebuildSession(self, req: sparkapi_pb2.RebuildRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        session.rebuild()

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f'Session: {req.session_id} rebuild',
        )

    def getSessionStatus(self, req: sparkapi_pb2.SessionStatusRequest, unused_context) -> sparkapi_pb2.StatusResponse:
        session = clientSessionTable.get_session(req.session_id)

        return sparkapi_pb2.StatusResponse(session_id=req.session_id, **session.get_session_status())

    # actions
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

    def previewDataset(self, req: sparkapi_pb2.PreviewDatasetRequest, unused_context) -> sparkapi_pb2.RowsResponse:
        session = clientSessionTable.get_session(req.session_id)
        node = session.plan.get_node_by_id(req.node_id)
        rows = session.preview(node, req.limit)
        return sparkapi_pb2.RowsResponse(row_json=rows)
