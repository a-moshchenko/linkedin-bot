import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


absolute_path = os.path.abspath('./database/linkedin_bot.db')
engine = create_engine(f'sqlite:////{absolute_path}',
                       echo=True)


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


Base.metadata.create_all(engine)


def get_all(table):
    objects = session.query(table)
    return objects


def create_user(table, **kwargs):
    if session.query(table).filter_by(id=kwargs['id']).count() < 1:
        obj = table(**kwargs)
        session.add(obj)
        session.commit()


def create_customer(table, **kwargs):
    obj = table(**kwargs)
    session.add(obj)
    session.commit()


def check_in_db(table, **kwargs):
    if session.query(table).filter_by(id=kwargs['name']).count() < 1:
        create_customer(table, **kwargs)
        return True
    return False


def create_message(**kwargs):
    obj = session.query(Message).get(1)
    if obj:
        obj.subject, obj.body = kwargs['subject'], kwargs['body']
    else:
        obj = Message(**kwargs)
        session.add(obj)
    session.commit()
