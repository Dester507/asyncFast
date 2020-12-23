from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from models import Base, User, Taxes
from config import HOST, PORT, DATABASE, USERNAME, PASSWORD

app = FastAPI()


class UserAPI(BaseModel):
    username: str
    name: str
    surname: str
    age: int


class TaxesAPI(BaseModel):
    username: str
    water: float
    light: float
    gaz: float


async def async_add_user():
    engine = create_async_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return {"engine": engine}


async def delete_info(session, username):
    user = session.query(User).filter(User.username == username).first()
    if user:
        session.query(Taxes).filter(Taxes.username == username).first().delete()
        return True
    else:
        return False


@app.post("/add")
async def add_user(user: UserAPI, taxes: TaxesAPI, eng: dict = Depends(async_add_user)):
    async with AsyncSession(eng['engine']) as session:
        async with session.begin():
            session.add(User(user.username, user.name, user.surname, user.age))
            session.add(Taxes(taxes.username, taxes.water, taxes.light, taxes.gaz))
        await session.commit()
    return {"Result": "Good"}


@app.post("/delete{username}")
async def remove_user(username: str, eng: dict = Depends(async_add_user)):
    async with AsyncSession(eng['engine']) as session:
        async with session.begin():
            status = await session.run_sync(delete_info, username)
            if status is False:
                return {"Error": "User with this username does not exists"}
        await session.commit()
    return {"Result": "Good"}
