from typing import Generator

import pytest
from app.infrastructure.sqlalchemy.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
