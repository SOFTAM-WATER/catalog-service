from enum import Enum

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.errors import AppError
from app.core.config import get_settings
from app.grpc.container import GrpcClients

from app.api.v1.handlers.products import router as products_router

settings = get_settings()
app = FastAPI()

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    code = exc.code.value if isinstance(exc.code, Enum) else exc.code

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": code,
            "message": exc.message,
            "details": exc.details if exc.details else "no details"
        }
    )

@app.on_event("startup")
async def startup():
    app.state.grpc = GrpcClients(settings)

app.include_router(products_router)

@app.on_event("shutdown")
async def shutdown():
    await app.state.grpc.close()