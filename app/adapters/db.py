from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

_engine = None
SessionLocal = None


def init_db(app):
    global _engine, SessionLocal
    db_url = app.config["DATABASE_URL"]
    _engine = create_engine(db_url, future=True)
    SessionLocal = scoped_session(sessionmaker(bind=_engine, autoflush=False, autocommit=False))


def get_session():
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db(app) first.")
    return SessionLocal()


def remove_session():
    if SessionLocal is not None:
        SessionLocal.remove()


def get_engine():
    return _engine
