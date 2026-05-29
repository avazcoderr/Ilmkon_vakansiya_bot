from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id         = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username   = Column(String(64), nullable=True)
    full_name  = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Application(Base):
    __tablename__ = "applications"
    id               = Column(Integer, primary_key=True, autoincrement=True)
    user_telegram_id = Column(BigInteger, nullable=False, index=True)
    position_key     = Column(String(32), nullable=False)
    position_label   = Column(String(64), nullable=False)
    # in_progress | completed | accepted | rejected | cancelled
    status           = Column(String(16), default="in_progress")
    created_at       = Column(DateTime, default=datetime.utcnow)
    completed_at     = Column(DateTime, nullable=True)


class Answer(Base):
    __tablename__ = "answers"
    id             = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, nullable=False, index=True)
    field_key      = Column(String(64), nullable=False)
    field_label    = Column(String(128), nullable=False)
    value          = Column(Text, nullable=True)
    value_type     = Column(String(16), default="text")   # text | photo | document
    created_at     = Column(DateTime, default=datetime.utcnow)


class ApplicationNote(Base):
    __tablename__ = "application_notes"
    id               = Column(Integer, primary_key=True, autoincrement=True)
    application_id   = Column(Integer, nullable=False, index=True)
    admin_telegram_id = Column(BigInteger, nullable=False)
    admin_name       = Column(String(128), nullable=True)
    text             = Column(Text, nullable=False)
    created_at       = Column(DateTime, default=datetime.utcnow)
