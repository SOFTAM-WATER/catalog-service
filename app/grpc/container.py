import grpc

from app.grpc.clients.user_client import UserClient

class GrpcClients:
    def __init__(self, settings):
        self.user_channel = grpc.aio.insecure_channel(settings.USER_SVC)

        self.user = UserClient(self.user_channel)
    
    async def close(self):
        await self.user_channel.close()
