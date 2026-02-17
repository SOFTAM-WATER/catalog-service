from enum import Enum
from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import text, DateTime
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID 

uuint_pk = Annotated[
	UUID,
	mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
]

uuid_ref = Annotated[
    UUID,
    mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
]

dt_now_utc_sql = text("now()")
created_at = Annotated[
    datetime,
    mapped_column(DateTime, server_default=dt_now_utc_sql, nullable=False, index=True)
]

closed_at = Annotated[
    datetime,
    mapped_column(DateTime(timezone=True), nullable=True)
]
