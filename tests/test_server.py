from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {
        "message": "inference API is healthy, and running",
        "data": {
            "name": "sentiment-analyzer",
            "version": "0.1.0",
        },
    }


def test_good_str_input():
    response = client.post("/invocations", json={"data": "sun is beautiful today"})
    assert response.status_code == 200
    assert response.json() == {
        "message": "model produced the prediction successfully",
        "sentiment": "positive"
    }


def test_good_lst_input():
    response = client.post("/invocations", json={"data": ["sun is beautiful today", "you are so bad, I hate you"]})
    assert response.status_code == 200
    assert response.json() == {
        "message": "model produced the prediction successfully",
        "sentiment": ["positive", "negative"]
    }


def test_wrong_str_input():
    response = client.post("/invocations", json={"data": 22})
    assert response.status_code == 422


def test_wrong_key_input():
    response = client.post("/invocations", json={"query": 22})
    assert response.status_code == 422
