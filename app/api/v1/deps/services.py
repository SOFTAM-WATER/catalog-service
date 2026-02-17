from fastapi import Depends

from app.schemas.products import CreateProductRequest, ProductResponce
from app.api.v1.services.product_service import ProductService
from app.utils.unit_of_work import UnitOfWork 

def get_product_service(uow: UnitOfWork = Depends()) -> ProductService:
    return ProductService(uow=uow)