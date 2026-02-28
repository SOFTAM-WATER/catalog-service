from uuid import UUID
from typing import Sequence

from sqlalchemy import select

from app.models.products import Product
from app.utils.repository import SQLAlchemyRepository

class ProductRepository(SQLAlchemyRepository[Product]):
    _model = Product
    
    async def get_by_ids(self, ids: Sequence[UUID]):
        stmt = select(self._model).where(self._model.id.in_(ids))
        result = await self.session.execute(stmt)
        return result.scalars().all()