from sqlalchemy.ext.asyncio import AsyncSession

from app.models.products import Product
from app.utils.repository import SQLAlchemyRepository

class ProductRepository(SQLAlchemyRepository[Product]):
    _model = Product
    