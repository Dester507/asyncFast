import asyncio

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from models import Base, User

app = FastAPI()


class UserAPI(BaseModel):
    name: str
    surname: str
    age: int


async def async_add_user(name=None, surname=None, age=None):
    engine = create_async_engine("sqlite:///data.db", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine) as session:
        async with session.begin():
            session.add(User(name, surname,  age))
        await session.commit()


@app.post("/add")
async def add_user(user: UserAPI):
    await async_add_user(user.name, user.surname, user.age)
    return {"Result": "Good"}
