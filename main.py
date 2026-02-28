from enum import Enum
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.database.db import engine
from app.core.errors import AppError
from app.core.config import get_settings
from app.grpc.container import GrpcClients
from app.api.v1.handlers.products import router as products_router
from app.api.v1.handlers.order_drafts import router as order_drafts_router
from scripts.init_models import init_models


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models(engine)

    grpc_clients = GrpcClients(settings)
    app.state.grpc = grpc_clients

    yield

app = FastAPI(lifespan=lifespan)


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


app.include_router(products_router)
app.include_router(order_drafts_router)


@app.on_event("shutdown")
async def shutdown():
    await app.state.grpc.close()