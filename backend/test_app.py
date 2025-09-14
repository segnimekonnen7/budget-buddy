"""Basic tests for the Habit Loop API."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import get_db, Base
from app.models import *

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    """Set up test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_request_magic_link(setup_database):
    """Test magic link request."""
    response = client.post("/auth/request-magic-link", json={"email": "test@example.com"})
    assert response.status_code == 200
    assert "message" in response.json()

def test_habits_endpoint_requires_auth():
    """Test that habits endpoint requires authentication."""
    response = client.get("/habits")
    assert response.status_code == 401

def test_create_habit_requires_auth():
    """Test that creating habits requires authentication."""
    response = client.post("/habits", json={
        "title": "Test Habit",
        "schedule_json": {"type": "daily"},
        "goal_type": "check"
    })
    assert response.status_code == 401

if __name__ == "__main__":
    pytest.main([__file__])
