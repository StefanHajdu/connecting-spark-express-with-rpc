import os

from grpc_tools import protoc

LIB_DIR = './lib'
os.makedirs(LIB_DIR, exist_ok=True)


protoc.main(
    (
        '',
        '-I../protos',
        f'--python_out={LIB_DIR}',
        f'--pyi_out={LIB_DIR}',
        f'--grpc_python_out={LIB_DIR}',
        '../protos/sparkapi.proto',
    )
)
