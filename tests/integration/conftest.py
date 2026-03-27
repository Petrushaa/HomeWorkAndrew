import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

TEST_DB_FILE = Path("tests/integration/test_app.db")
os.environ["DB_URL"] = f"sqlite:///{TEST_DB_FILE}"

from core.database import Base, SessionLocal, engine, get_db
from core.dependency import get_current_user
from main import app
from models.users import User


@pytest.fixture()
def db_session() -> Session:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session: Session):
    test_user = User(
        username="integration_user",
        email="integration_user@example.com",
        hashed_password="hashed_password",
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    def override_get_current_user():
        return test_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
