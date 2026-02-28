import grpc

from app.grpc.clients.user_client import UserClient
from app.grpc.clients.order_draft_client import OrderDraftClient

class GrpcClients:
    def __init__(self, settings):
        self.user_channel = grpc.aio.insecure_channel(settings.USER_SVC)
        self.order_channel = grpc.aio.insecure_channel(settings.ORDER_SVC)

        self.user = UserClient(self.user_channel)
        self.order = OrderDraftClient(self.order_channel)
    
    async def close(self):
        await self.user_channel.close()
