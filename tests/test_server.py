import pytest

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.mark.xfail(reason="Test don't see /static folder(while to imported app is mounted static folder)"
                          " and there is Authorization Exception (401 code): the endpoint is saved")
def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
