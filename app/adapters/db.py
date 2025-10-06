from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

_engine = None
SessionLocal = None


def init_db(app: Flask) -> None:
    global _engine, SessionLocal
    db_url = app.config["DATABASE_URL"]
    _engine = create_engine(db_url, future=True)
    SessionLocal = scoped_session(sessionmaker(bind=_engine, autoflush=False, autocommit=False))


def get_session() -> Session:
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db(app) first.")
    return SessionLocal()


def remove_session() -> None:
    if SessionLocal is not None:
        SessionLocal.remove()


def get_engine() -> Engine | None:
    return _engine
