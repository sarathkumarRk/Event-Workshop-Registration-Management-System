import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient

import app.database as database


TEST_DATABASE_URL = "sqlite://"


test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


database.engine = test_engine
database.SessionLocal = TestingSessionLocal


from app import models
from app.main import app


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


app.dependency_overrides[
    database.get_db
] = override_get_db


@pytest.fixture
def client():

    database.Base.metadata.drop_all(
        bind=test_engine
    )

    database.Base.metadata.create_all(
        bind=test_engine
    )

    with TestClient(app) as test_client:
        yield test_client

    database.Base.metadata.drop_all(
        bind=test_engine
    )


@pytest.fixture
def db():

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


@pytest.fixture
def participant_token(client):

    response = client.post(
        "/auth/register",
        json={
            "full_name": "Test Participant",
            "email": "participant@test.com",
            "password": "password123",
            "role": "participant"
        }
    )

    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": "participant@test.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture
def admin_token(client):

    response = client.post(
        "/auth/register",
        json={
            "full_name": "Test Admin",
            "email": "admin@test.com",
            "password": "password123",
            "role": "admin"
        }
    )

    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]