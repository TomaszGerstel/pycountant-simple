import pytest

from app.main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
