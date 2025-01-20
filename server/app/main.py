from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import values
from app.services.database import engine


# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(values.router)
