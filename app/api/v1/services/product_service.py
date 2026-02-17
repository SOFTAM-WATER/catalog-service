from uuid import UUID

from app.utils.service import BaseService, transaction_mode
from app.schemas.products import CreateProductRequest
from app.utils.error_codes import ErrorCode


class ProductService(BaseService):
    _repo: str = 'product'

    @transaction_mode
    async def create_product(self, product: CreateProductRequest):
        created_product = await self.uow.product.add_one_and_get_obj(**product.model_dump())
        return created_product.to_schema()
    
    @transaction_mode
    async def get_product_by_id(self, product_id: UUID):
        product = await self.uow.product.get_by_filter_one_or_none(id=product_id)
        self.check_existence(obj=product, details=ErrorCode.PRODUCT_NOT_FOUND)
        assert product is not None
        return product.to_schema()
