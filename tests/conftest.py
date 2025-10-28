"""Pytest configuration and fixtures for API tests."""
import pytest
from fastapi.testclient import TestClient

from database import InMemoryDatabase
from main import app


@pytest.fixture
def db():
    """Provide a fresh database instance for each test."""
    return InMemoryDatabase()


@pytest.fixture
def client(db, monkeypatch):
    """Provide a TestClient with a fresh database instance."""
    import database
    monkeypatch.setattr(database, "db", db)
    
    # Re-import main to use the patched database
    import importlib
    import main
    importlib.reload(main)
    
    return TestClient(main.app)
