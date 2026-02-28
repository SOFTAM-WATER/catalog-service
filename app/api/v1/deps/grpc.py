from fastapi import Request
from app.grpc.container import GrpcClients

def get_grpc_clients(request: Request) -> GrpcClients:
    return request.app.state.grpc