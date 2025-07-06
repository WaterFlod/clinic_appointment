from fastapi import FastAPI
import uvicorn
from routers import router

from database import Base, engine

import asyncio

app = FastAPI()


app.include_router(router)

async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            

if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run("main:app", log_level="info", host="0.0.0.0")