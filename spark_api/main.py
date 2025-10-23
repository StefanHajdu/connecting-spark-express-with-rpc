from concurrent import futures

import grpc
from sparkapi_pb2_grpc import add_SparkApiServicer_to_server

from core.spark_proxy import SparkRpcApi


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SparkApiServicer_to_server(SparkRpcApi(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
