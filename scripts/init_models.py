import asyncio

from app.database.db import engine, Base
import app.models.products

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

asyncio.run(init_models())