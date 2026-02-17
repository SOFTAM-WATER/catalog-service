from typing import Optional, Any
from starlette.status import HTTP_400_BAD_REQUEST

class AppError(Exception):
    def __init__(
        self,
        message: str,
        code: str = "APP_ERROR",
        status_code: int = HTTP_400_BAD_REQUEST,
        details: Optional[Any] = None
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details