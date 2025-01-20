import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import values
from app.services.database import engine

logging.basicConfig(
    level=logging.INFO,  # Mức độ log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Định dạng log
    handlers=[
        logging.FileHandler("app.log"),  # Ghi log vào file
        logging.StreamHandler(),  # Hiển thị log trên console
    ],
)


# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "http://localhost:3050",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(values.router)
