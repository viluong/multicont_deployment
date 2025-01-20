import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.value import ValueRequest
from app.services.database import get_db
from app.services.redis import get_redis

router = APIRouter(prefix="/values", tags=["values"])

logger = logging.getLogger(__name__)


@router.get("/all")
async def get_all_values(db: AsyncSession = Depends(get_db)):
    logger.info("111111111111111111111111")
    result = await db.execute(text("SELECT * FROM values"))
    values = [dict(row) for row in result.mappings()]
    return values


@router.get("/current")
async def get_current_values(redis=Depends(get_redis)):
    values = await redis.hgetall("values")
    return values


@router.post("")
async def create_value(
    value: ValueRequest, db: AsyncSession = Depends(get_db), redis=Depends(get_redis)
):
    if value.index > 40:
        raise HTTPException(status_code=422, detail="Index too high")

    await redis.hset("values", value.index, "Nothing yet!")
    await redis.publish("insert", value.index)

    await db.execute(text(f"INSERT INTO values(number) VALUES({value.index})"))

    return {"working": True}
