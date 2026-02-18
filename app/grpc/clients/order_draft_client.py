from uuid import UUID, uuid4

import grpc
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_504_GATEWAY_TIMEOUT,
    HTTP_503_SERVICE_UNAVAILABLE,
    HTTP_502_BAD_GATEWAY,
)

from google.type import date_pb2
from google.type import timeofday_pb2

from app.core.errors import AppError
from app.utils.error_codes import ErrorCode
from app.schemas.order_drafts import CreateOrderDraftRequest
import app.grpc.generated.order_draft_pb2 as draft_pb2
import app.grpc.generated.order_draft_pb2_grpc as draft_pb2_grpc


class OrderDraftClient:
    def __init__(self, channel: grpc.aio.Channel) -> None:
        self._stub = draft_pb2_grpc.OrderServiceStub(channel)
    
    async def create_order_draft(self, user_id: UUID, payload: CreateOrderDraftRequest):
        delivery_date = payload.delivery_date
        slot_from = payload.slot_from
        slot_to = payload.slot_to

        request = draft_pb2.CreateOrderRequest(
            transaction_id=str(uuid4()),
            user_id=str(user_id),
            full_name=payload.full_name,
            phone=payload.phone,
            location=payload.location,
            total_sum=sum(item.quantity * item.price for item in payload.items),
            delivery_date=date_pb2.Date(
                year=delivery_date.year,
                month=delivery_date.month,
                day=delivery_date.day
            ),
            slot_from=timeofday_pb2.TimeOfDay(
                hours=slot_from.hour,
                minutes=slot_from.minute,
            ),
            slot_to=timeofday_pb2.TimeOfDay(
                hours=slot_to.hour,
                minutes=slot_to.minute,
            ),
            items=[
                draft_pb2.OrderItem(
                    product_id=str(item.product_id),
                    quantity=item.quantity,
                    subtotal_price=item.quantity * item.price
                )
                for item in payload.items
            ]
        )

        try:
            resp = await self._stub.CreateOrderFromDraft(request, timeout=2.0)
            return UUID(resp.user_id)
        
        except grpc.aio.AioRpcError as e:
            self._handle_grpc_error(e)
            
        
    def _handle_grpc_error(self, e: grpc.aio.AioRpcError):
        code = e.code()
        
        raise AppError("Order Service Error.", ErrorCode.ORDER_SVC_ERROR, HTTP_502_BAD_GATEWAY)