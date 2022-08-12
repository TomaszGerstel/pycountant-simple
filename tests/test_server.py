import pytest

from app.main import app
from fastapi.testclient import TestClient


client = TestClient(app)


@pytest.mark.xfail(reason="Need to mock DB for CI tests")
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
