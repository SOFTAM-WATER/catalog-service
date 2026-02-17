from uuid import UUID

from pydantic import BaseModel, Field

class ProductID(BaseModel):
    id: UUID


class CreateProductRequest(BaseModel):
    name: str = Field(max_length=256)
    volume: float = Field()
    price: int = Field()


class ProductResponce(BaseModel):
    id: UUID
    name: str
    volume: float
    price: int

    class Config:
        from_attributes = True


class ProductDB(ProductID, CreateProductRequest):
    pass