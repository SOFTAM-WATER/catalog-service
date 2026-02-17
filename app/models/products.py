from sqlalchemy import String, Integer, Float, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.db import Base
from app.utils.custom_types import uuint_pk
from app.schemas.products import ProductDB

class BaseModel(Base):
    __abstract__ = True

class Product(BaseModel):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_product_price_gte_0"),
        CheckConstraint("volume > 0", name="ck_product_volume_gt_0")
    )

    id: Mapped[uuint_pk]
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    volume: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    def to_schema(self) -> ProductDB:
        return ProductDB(**self.__dict__)