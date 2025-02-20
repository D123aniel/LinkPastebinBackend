from fastapi.testclient import TestClient
from fastapi.responses import RedirectResponse
from main import app

client = TestClient(app)


def test_sue_text_posting():
    """Test that the /create-text endpoint handles creating a new pastebin link correctly."""
    response = client.post(
        "/create-text",
        json={
            "id": "",
            "content": "Hello World",
            "vanity_url": "exam-solutions",
            "type": "text",
            "expiration_time": -1,
        },
    )

    assert response.status_code == 201
    assert response.headers["content-type"] == "application/json"

    data = response.json()
    assert "id" in data
    assert "content" in data
    assert "vanity_url" in data
    assert "type" in data
    assert "expiration_time" in data
    assert "access_count" in data

    assert data["id"] == "exam-solutions"
    assert data["content"] == "Hello World"
    assert data["vanity_url"] == "exam-solutions"
    assert data["type"] == "text"
    assert data["expiration_time"] is not None
    assert data["access_count"] == 0
