from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError, ExpiredSignatureError
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from app.core.config import get_settings
from app.core.errors import AppError
from app.utils.error_codes import ErrorCode

settings = get_settings()
security = HTTPBearer()


class SecurityUtils:
    @staticmethod
    def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

            if payload.get("sub") is None:
                raise AppError("JWT missing subject", ErrorCode.JWT_INVALID, HTTP_401_UNAUTHORIZED)   
             
        except ExpiredSignatureError:
            raise AppError("JWT expired", ErrorCode.JWT_EXPIRED, HTTP_401_UNAUTHORIZED)
        except JWTError:
            raise AppError("JWT invalid", ErrorCode.JWT_INVALID, HTTP_401_UNAUTHORIZED)
        