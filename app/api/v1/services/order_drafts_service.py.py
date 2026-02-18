from uuid import UUID

from starlette.status import HTTP_404_NOT_FOUND

from app.core.errors import AppError
from app.utils.service import BaseService, transaction_mode
from app.schemas.order_drafts import CreateOrderDraftRequest
from app.utils.error_codes import ErrorCode


class OrderDraftService(BaseService):
    _repo: str | None = None
    
    @transaction_mode
    async def create_order_draft(self, draft: CreateOrderDraftRequest):
        user_id: UUID | None = None

        if draft.telegram_id:
            user_id = await self.uow.users.validate_user(
                telegram_id=draft.telegram_id,
                phone=draft.phone,
                full_name=draft.full_name
            )

        product_ids = [item.product_id for item in draft.items]

        products = await self.uow.product.get_by_filter_all(
            *product_ids
        )

        if len(products) != len(product_ids):
            raise AppError(
                "Some products not found", 
                ErrorCode.PRODUCT_NOT_FOUND, 
                HTTP_404_NOT_FOUND
            )

        

        
