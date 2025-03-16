import grpc

import sparkapi_pb2

from concurrent import futures
from typing import Iterable
from sparkapi_pb2_grpc import (
    SparkApiServicer,
    add_SparkApiServicer_to_server,
)

from ClientSession import ClientSession
from ClientSessionTable import ClientSessionTable
from PipelinePlan import SessionPlanner, SessionPlannerMap

clientSessionTable = ClientSessionTable()
sessionPlannerMap = SessionPlannerMap(clientSessionTable)


class SparkApiServicer(SparkApiServicer):
    def createSession(self, req: sparkapi_pb2.NewSessionRequest, unused_context) -> sparkapi_pb2.NewSessionResponse:
        clientSessionTable.add(req.id, ClientSession(req.id))
        sessionPlannerMap.add_session(req.id)

        return sparkapi_pb2.NewSessionResponse(
            id=req.id,
            msg=f"Session {req.id} created.",
        )

    def loadsDataset(
        self, req: sparkapi_pb2.LoadDatasetRequest, unused_context
    ) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        root_plan_node = session.load_dataset(req.df_path, req.df_type)
        session.plan = SessionPlanner(req.session_id, root_plan_node)
        sessionPlannerMap.update_session_plan(session.id, session.plan)

        return sparkapi_pb2.SparkTransformResponse(session_id=req.session_id, msg=f"Dataset {req.df_path} loaded.")

    def loadFromSession(
        self, req: sparkapi_pb2.LoadFromSessionRequest, unused_context
    ) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)

        parent_session = clientSessionTable.get_session(req.input_session_id)
        parent_session_plan = sessionPlannerMap.get_session_plan(req.input_session_id)
        root_plan_node = session.load_from_session(parent_session, parent_session_plan)

        session.plan = SessionPlanner(req.session_id, root_plan_node)
        sessionPlannerMap.update_session_plan(session.id, session.plan)

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f"Dataframe from input session {req.input_session_id} reused input.",
        )

    def create_FilterNode(
        self, req: sparkapi_pb2.FilterNodeRequest, unused_context
    ) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        session.add_filter_node(
            node_id=req.node_id,
            prev_node_id=req.prev_node_id,
            expressions=list(req.expressions),
            matching=req.matching,
        )

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f"Node: {req.node_id} added and transform",
        )

    def edit_FilterNode(
        self, req: sparkapi_pb2.FilterNodeRequest, unused_context
    ) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        session.edit_filter_node(req.node_id, list(req.expressions), req.matching)

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f"Node: {req.node_id} edited",
        )

    def create_AddColumnNode(
        self, req: sparkapi_pb2.AddColumnNodeRequest, unused_context
    ) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        session.add_addColumn_node(
            node_id=req.node_id,
            prev_node_id=req.prev_node_id,
            expressions=list(req.expressions),
        )

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f"Node: {req.node_id} added and transform",
        )

    def edit_AddColumnNode(
        self, req: sparkapi_pb2.AddColumnNodeRequest, unused_context
    ) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        session.edit_addColumn_node(req.node_id, list(req.expressions))

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f"Node: {req.node_id} edited",
        )

    def removeNode(
        self, req: sparkapi_pb2.NodeRemovalRequest, unused_context
    ) -> sparkapi_pb2.PysparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        session.remove_node(req.node_id)

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f"Node: {req.node_id} removed",
        )

    def rebuildSession(
        self, req: sparkapi_pb2.RebuildRequest, unused_context
    ) -> sparkapi_pb2.PysparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        session.rebuild()

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f"Session: {req.session_id} rebuild",
        )

    def summarizeDataset(
        self, req: sparkapi_pb2.SummarizeDatasetRequest, unused_context
    ) -> sparkapi_pb2.SparkActionlResponse:
        session = clientSessionTable.get_session(req.session_id)
        summary = session.summarize(req.node_id)

        return sparkapi_pb2.SparkActionlResponse(
            session_id=req.session_id,
            msg=f"Node {req.node_id} summarized",
            columns=summary["columns"],
            count=summary["count"],
            schema=summary["schema"],
        )

    def previewDataset(
        self, req: sparkapi_pb2.PreviewDatasetRequest, unused_context
    ) -> Iterable[sparkapi_pb2.RowStreamResponse]:
        session = clientSessionTable.get_session(req.session_id)
        row_stream = session.preview(req.node_id, req.limit)

        for row in row_stream:
            yield sparkapi_pb2.RowStreamResponse(row_json=row)

    def getSessionStatus(self, req: sparkapi_pb2.SessionStatusRequest, unused_context) -> sparkapi_pb2.StatusResponse:
        session = clientSessionTable.get_session(req.session_id)

        return sparkapi_pb2.StatusResponse(session_id=req.session_id, **session.get_session_status())


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SparkApiServicer_to_server(SparkApiServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
