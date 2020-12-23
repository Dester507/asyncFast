from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Float

Base = declarative_base()


class User(Base):
    __tablename__ = "users_api"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    def __init__(self, username, name, surname, age):
        self.username = username
        self.name = name
        self.surname = surname
        self.age = age


class Taxes(Base):
    __tablename__ = 'taxes_api'

    id = Column(Integer, primary_key=True)
    person = Column(String, unique=True)
    water = Column(Float, nullable=False)
    light = Column(Float, nullable=False)
    gaz = Column(Float, nullable=False)

    def __init__(self, person, water, light, gaz):
        self.person = person
        self.water = water
        self.light = light
        self.gaz = gaz
