from uuid import UUID
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Never, Any

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from app.models.products import BaseModel

T = TypeVar("T", bound=BaseModel)

class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError

    async def add_one_and_get_id(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError
    
    async def add_one_and_get_obj(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError
    
    async def get_by_filter_one_or_none(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError
    

class SQLAlchemyRepository(AbstractRepository, Generic[T]):
    _model: type[T]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, **kwargs: Any) -> None:
        stmt = insert(self._model).values(**kwargs).returning(self._model)
        await self.session.execute(stmt)
    
    async def add_one_and_get_id(self, **kwargs: Any) -> int | str | UUID:
        stmt = insert(self._model).values(**kwargs).returning(self._model.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def add_one_and_get_obj(self, **kwargs: Any) -> T:
        stmt = insert(self._model).values(**kwargs).returning(self._model)
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def get_by_filter_one_or_none(self, **kwargs: Any) -> T | None:
        stmt = select(self._model).filter_by(**kwargs)
        result: Result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()
        
