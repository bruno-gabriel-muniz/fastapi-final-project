import pytest
from fastapi.testclient import TestClient

from src.tcc_madrs.app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
