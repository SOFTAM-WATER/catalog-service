from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT 

from app.api.v1.deps.services import get_product_service
from app.schemas.products import CreateProductRequest, ProductResponce
from app.api.v1.services.product_service import ProductService



router = APIRouter(prefix="/products")

@router.post(
    path="/create",
    status_code=HTTP_201_CREATED,
    response_model=ProductResponce
)
async def create_product(
    product: CreateProductRequest,
    service: ProductService = Depends(get_product_service)
):
    return await service.create_product(product)


@router.get(
    path="/{product_id}",
    status_code=HTTP_200_OK
)
async def get_product(
    product_id: UUID,
    service: ProductService = Depends(get_product_service)
):
    return await service.get_product_by_id(product_id)