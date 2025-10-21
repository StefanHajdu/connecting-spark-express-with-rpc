import os

from grpc_tools import protoc

CORE_DIR = './core'
os.makedirs(CORE_DIR, exist_ok=True)


protoc.main(
    (
        '',
        '-I../protos',
        f'--python_out={CORE_DIR}',
        f'--pyi_out={CORE_DIR}',
        f'--grpc_python_out={CORE_DIR}',
        '../protos/sparkapi.proto',
    )
)
