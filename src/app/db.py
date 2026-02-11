# FILE: src/app/db.py

import os
from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    SmallInteger,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)

Base = declarative_base()


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Float, nullable=False)
    bmi = Column(Float, nullable=False)
    avg_glucose_level = Column(Float, nullable=False)
    hypertension = Column(SmallInteger, nullable=False)
    heart_disease = Column(SmallInteger, nullable=False)
    severity = Column(String(32), nullable=False)
    model = Column(String(64), nullable=False)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
