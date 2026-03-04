from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_test_endpoint():
    res = client.get("/test")
    assert res.status_code == 200
    assert res.json()["message"] == "It is working"