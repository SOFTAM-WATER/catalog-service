from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ValidateUserRequest(_message.Message):
    __slots__ = ("telegram_id", "phone", "full_name")
    TELEGRAM_ID_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    telegram_id: int
    phone: str
    full_name: str
    def __init__(self, telegram_id: _Optional[int] = ..., phone: _Optional[str] = ..., full_name: _Optional[str] = ...) -> None: ...

class ValidateUserResponse(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...
