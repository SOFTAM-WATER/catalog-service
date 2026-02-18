import grpc
from uuid import UUID
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_504_GATEWAY_TIMEOUT,
    HTTP_503_SERVICE_UNAVAILABLE,
    HTTP_502_BAD_GATEWAY,
)

import app.grpc.generated.user_service_pb2 as user_pb2
import app.grpc.generated.user_service_pb2_grpc as user_pb2_grpc
from app.core.errors import AppError
from app.utils.error_codes import ErrorCode


class UserClient:
    def __init__(self, channel: grpc.aio.Channel):
        self._stub = user_pb2_grpc.UserServiceStub(channel)

    async def validate_user(
        self,
        *,
        telegram_id: int,
        phone: str = "",
        full_name: str = ""
    ) -> UUID:

        request = user_pb2.ValidateUserRequest(
            telegram_id=telegram_id,
            phone=phone,
            full_name=full_name
        )

        try:
            resp = await self._stub.ValidateTelegramUser(request, timeout=2.0)
            return UUID(resp.user_id)

        except grpc.aio.AioRpcError as e:
            self._handle_grpc_error(e)
            
        
    def _handle_grpc_error(self, e: grpc.aio.AioRpcError):
        code = e.code()

        # transport / infra
        if code == grpc.StatusCode.DEADLINE_EXCEEDED:
            raise AppError("User service timeout.", ErrorCode.USER_SVC_TIMEOUT, HTTP_504_GATEWAY_TIMEOUT)
        if code in (grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.RESOURCE_EXHAUSTED):
            raise AppError("User service unuvailable.", ErrorCode.USER_SVC_UNAVAILABLE, HTTP_503_SERVICE_UNAVAILABLE)
            
        #business errors from user_service
        if code == grpc.StatusCode.INVALID_ARGUMENT:
            raise AppError("Invalid user data", ErrorCode.USER_INVALID_DATA, HTTP_400_BAD_REQUEST)
        if code == grpc.StatusCode.NOT_FOUND:
            raise AppError("User not found", ErrorCode.USER_NOT_FOUND, HTTP_404_NOT_FOUND)
        if code == grpc.StatusCode.PERMISSION_DENIED:
            raise AppError("User is blocked", ErrorCode.USER_BLOCKED, HTTP_403_FORBIDDEN)
        
        raise AppError("User Service Error.", ErrorCode.USER_SVC_ERROR, HTTP_502_BAD_GATEWAY)
