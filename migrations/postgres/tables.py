from typing import Type

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import INTEGER, TEXT
from sqlalchemy.ext.declarative import declarative_base


Base: Type = declarative_base()


class Users(Base):

    """
    Users table
    """

    __tablename__ = "users"

    user_id = Column(INTEGER, primary_key=True)
    email = Column(String(256), nullable=False, unique=True)
    password = Column(TEXT, nullable=False)


class Tasks(Base):

    """
    Tasks table
    """

    __tablename__ = "tasks"

    task_id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey("users.user_id"), nullable=False)
    title = Column(TEXT, nullable=False)
    description = Column(TEXT, nullable=True)
    status = Column(String(256), nullable=False)
    created_at = Column(DateTime)
