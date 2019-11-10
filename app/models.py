from datetime import datetime
from . import db
from sqlalchemy import Column, Integer, String, DateTime, Table
from sqlalchemy.sql import func
from uuid import uuid4


class User(db.Model):
    """Data model for Users"""

    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=uuid4)
    first_name = Column(String(64), index=True)
    last_name = Column(String(64), index=True)
    email = Column(String(120), index=True, unique=True)
    datecreated = Column(DateTime(timezone=True),
                             server_default=func.now())
    lastviewed = Column(DateTime, default=None)
    profpic = Column(String(128), default=None)
