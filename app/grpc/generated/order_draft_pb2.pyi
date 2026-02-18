from google.type import date_pb2 as _date_pb2
from google.type import timeofday_pb2 as _timeofday_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrderItem(_message.Message):
    __slots__ = ("product_id", "quantity", "subtotal_price")
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    SUBTOTAL_PRICE_FIELD_NUMBER: _ClassVar[int]
    product_id: str
    quantity: int
    subtotal_price: int
    def __init__(self, product_id: _Optional[str] = ..., quantity: _Optional[int] = ..., subtotal_price: _Optional[int] = ...) -> None: ...

class CreateOrderRequest(_message.Message):
    __slots__ = ("transaction_id", "user_id", "full_name", "phone", "location", "total_sum", "delivery_date", "slot_from", "slot_to", "items")
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SUM_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_DATE_FIELD_NUMBER: _ClassVar[int]
    SLOT_FROM_FIELD_NUMBER: _ClassVar[int]
    SLOT_TO_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    transaction_id: str
    user_id: str
    full_name: str
    phone: str
    location: str
    total_sum: int
    delivery_date: _date_pb2.Date
    slot_from: _timeofday_pb2.TimeOfDay
    slot_to: _timeofday_pb2.TimeOfDay
    items: _containers.RepeatedCompositeFieldContainer[OrderItem]
    def __init__(self, transaction_id: _Optional[str] = ..., user_id: _Optional[str] = ..., full_name: _Optional[str] = ..., phone: _Optional[str] = ..., location: _Optional[str] = ..., total_sum: _Optional[int] = ..., delivery_date: _Optional[_Union[_date_pb2.Date, _Mapping]] = ..., slot_from: _Optional[_Union[_timeofday_pb2.TimeOfDay, _Mapping]] = ..., slot_to: _Optional[_Union[_timeofday_pb2.TimeOfDay, _Mapping]] = ..., items: _Optional[_Iterable[_Union[OrderItem, _Mapping]]] = ...) -> None: ...

class OrderResponse(_message.Message):
    __slots__ = ("order_id", "status")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    status: str
    def __init__(self, order_id: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...
