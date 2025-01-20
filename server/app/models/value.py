from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Value(Base):
    __tablename__ = "values"
    number = Column(Integer, primary_key=True)


class ValueRequest(BaseModel):
    index: int