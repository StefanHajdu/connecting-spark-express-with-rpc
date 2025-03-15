import os

from grpc_tools import protoc

GENERATED_ROOT = './generated'
os.makedirs(GENERATED_ROOT, exist_ok=True)


protoc.main(
    (
        '',
        '-I../protos',
        f'--python_out={GENERATED_ROOT}',
        f'--grpc_python_out={GENERATED_ROOT}',
        '../protos/sparkapi.proto',
    )
)
