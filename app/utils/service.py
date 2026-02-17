import functools
from abc import ABC, abstractmethod
from uuid import UUID
from typing import (
    TypeVar, 
    Any, 
    Callable, 
    Awaitable, 
    overload, 
    Never
)

from starlette.status import HTTP_404_NOT_FOUND

from app.core.errors import AppError
from app.utils.error_codes import ErrorCode
from app.utils.repository import AbstractRepository
from app.utils.unit_of_work import AbstractUnitOfWork, UnitOfWork

T = TypeVar('T', bound=Callable[..., Awaitable[Any]])

@overload
def transaction_mode(_func: T) -> T: ...
@overload
def transaction_mode(*, auto_flush: bool) -> Callable[[T], T]: ...

def transaction_mode(
    _func: T | None = None, 
    *, 
    auto_flush: bool = False
) -> T | Callable[[T], T]:
    def decorator(func: T) -> T:
        @functools.wraps(func)
        async def wrapper(self: AbstractService, *args: Any, **kwargs: Any) -> Any:
            if self.uow.is_open:
                res = await func(self, *args, **kwargs)
                if auto_flush:
                    await self.uow.flush()
                return res
            async with self.uow:
                return await func(self, *args, **kwargs)
        
        return wrapper #type:ignore
    
    if _func is None:
        return decorator
    return decorator(_func)


class AbstractService(ABC):
    uow: AbstractUnitOfWork

    @abstractmethod
    async def add_one(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError

    async def add_one_and_get_id(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError
    
    async def add_one_and_get_obj(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError
    

class BaseService(AbstractService):
    _repo: str | None = None

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow : UnitOfWork = uow

        if not hasattr(self, '_repo') or self._repo is None:
            err_msg = f"Attribute '_repo' is required for class {self.__class__.__name__}"
            raise AttributeError(err_msg)
        
    def _get_related_repo(self) -> AbstractRepository:
        return getattr(self.uow, self._repo)
    
    @staticmethod
    def check_existence(obj: Any, details: str) -> None:
        if not obj:
            raise AppError(
                message=details,
                code="NOT_FOUND",
                status_code=404
            )
        
    @transaction_mode
    async def add_one(self, **kwargs: Any) -> None:
        await self._get_related_repo().add_one(**kwargs)

    @transaction_mode
    async def add_one_and_get_id(self, **kwargs: Any) -> int | str | UUID:
        return await self._get_related_repo().add_one_and_get_id(**kwargs)
    
    @transaction_mode
    async def add_one_and_get_obj(self, **kwargs: Any) -> Any:
        return await self._get_related_repo().add_one_and_get_obj(**kwargs)