from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.api.v1.deps.services import get_order_drafrs_service
from app.schemas.order_drafts import CreateOrderDraftRequest
from app.api.v1.services.order_drafts_service import OrderDraftService

router = APIRouter(prefix="/orders")

@router.post(
    path="/create",
    status_code=HTTP_201_CREATED,
)
async def create_order_draft(
    order: CreateOrderDraftRequest,
    service: OrderDraftService = Depends(get_order_drafrs_service)
):
    return await service.create_order_draft(order)