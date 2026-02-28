from fastapi import Depends

from app.api.v1.services.product_service import ProductService
from app.api.v1.services.order_drafts_service import OrderDraftService
from app.utils.unit_of_work import UnitOfWork 

def get_product_service(uow: UnitOfWork = Depends()) -> ProductService:
    return ProductService(uow=uow)

def get_order_drafrs_service(uow: UnitOfWork = Depends()) -> OrderDraftService:
    return OrderDraftService(uow=uow)