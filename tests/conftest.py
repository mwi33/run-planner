import os
import tempfile

import pytest

from app import create_app
from app.adapters.db import get_engine
from app.domain.models import Base


@pytest.fixture(scope="session")
def app_instance():
    # Use a temp SQLite DB file per session
    db_fd, db_path = tempfile.mkstemp()
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    app = create_app()
    with app.app_context():
        engine = get_engine()
        Base.metadata.create_all(bind=engine)
    yield app
    os.close(db_fd)
    try:
        os.remove(db_path)
    except FileNotFoundError:
        pass


@pytest.fixture()
def client(app_instance):
    return app_instance.test_client()
