from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database/linkedin_bot.db',
                       echo=False)


Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    login = Column(String(100))
    password = Column(String(100))


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    subject = Column(String(100))
    body = Column(Text)


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    url = Column(String(255))


# Base.metadata.create_all(engine)


def create(cls, **kwargs):
    obj = User(**kwargs)
    session.add(obj)
    session.commit()
