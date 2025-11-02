import grpc
import sparkapi_pb2_grpc


class RpcClient:
    """Singleton gRPC client for Spark API communication."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # Create gRPC channel and stub
        self.channel = grpc.insecure_channel('localhost:50051')
        self.client = sparkapi_pb2_grpc.SparkApiStub(self.channel)
        self._initialized = True

    def __del__(self):
        if hasattr(self, 'channel'):
            self.channel.close()
