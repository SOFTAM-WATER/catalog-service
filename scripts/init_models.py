import asyncio

from sqlalchemy import text

import app.models.products
from app.database.db import engine, Base

async def init_models(engine):
    retries = 5
    while retries > 0:
        try:
            async with engine.begin() as conn:

                await conn.execute(text("SELECT 1"))
                
                await conn.run_sync(Base.metadata.create_all)
            print("Таблицы успешно созданы!")
            break
        except Exception as e:
            retries -= 1
            print(f"База еще не готова, ждем... ({retries} попыток осталось). Ошибка: {e}")
            await asyncio.sleep(2)