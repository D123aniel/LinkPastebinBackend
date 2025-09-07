from fastapi.testclient import TestClient
from fastapi.responses import RedirectResponse
from main import app


def test_dummy():
    assert True == True


# client = TestClient(app)


# def test_sue_text_posting():
#     """Test that the /create-text endpoint handles creating a new pastebin link correctly."""
#     response = client.post(
#         "/create-text",
#         json={
#             "id": "",
#             "content": "Hello World",
#             "vanity_url": "exam-solutions",
#             "type": "text",
#             "expiration_time": -1,
#         },
#     )

#     assert response.status_code == 201
#     assert response.headers["content-type"] == "application/json"

#     data = response.json()
#     assert "id" in data
#     assert "content" in data
#     assert "vanity_url" in data
#     assert "type" in data
#     assert "expiration_time" in data
#     assert "access_count" in data

#     assert data["id"] == "exam-solutions"
#     assert data["content"] == "Hello World"
#     assert data["vanity_url"] == "exam-solutions"
#     assert data["type"] == "text"
#     assert data["expiration_time"] is not None
#     assert data["access_count"] == 0


# def test_sue_link_shortening():
#     """Test that the /shorten-url endpoint handles shortening a longer link correctly."""
#     response = client.post(
#         "/shorten-url",
#         json={
#             "id": "",
#             "content": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
#             "vanity_url": "query-stuff",
#             "type": "link",
#         },
#     )

#     assert response.status_code == 201
#     assert response.headers["content-type"] == "application/json"

#     data = response.json()
#     assert "id" in data
#     assert "content" in data
#     assert "vanity_url" in data
#     assert "type" in data
#     assert "expiration_time" in data
#     assert "access_count" in data

#     assert data["id"] == "query-stuff"
#     assert data["content"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
#     assert data["vanity_url"] == "query-stuff"
#     assert data["type"] == "link"
#     assert data["expiration_time"] is not None
#     assert data["access_count"] == 0


# def test_cai_clicking_text_link():
#     """Test that the /{resource_id} endpoint handles accessing a pastebin link correctly."""
#     response = client.get("/exam-solutions")

#     assert response.status_code == 200
#     assert response.headers["content-type"] == "application/json"

#     data = response.json()
#     assert "Hello World" == data


# def test_cai_clicking_shortened_link():
#     """Test that the /{resource_id} endpoint handles accessing a shortened url correctly."""
#     response = client.get("/query-stuff", follow_redirects=False)

#     assert response.status_code == 307
#     assert response.headers["location"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

#     # def test_amy_retrieving_resources():
#     #     """Test that the /admin/resources endpoint retrieves all resources correctly."""
#     #     response = client.get("/admin/resources")

#     assert response.status_code == 200
#     assert response.headers["content-type"] == "application/json"

#     data = response.json()
#     assert len(data) == 2
#     assert data[0]["id"] == "exam-solutions"
#     assert data[1]["id"] == "query-stuff"


# def test_amy_retrieving_access_count():

#     """Test that the /admin/resources/{resource_id} endpoint retrieves resource view counts correctly."""
#     response = client.get("/admin/resources/exam-solutions")

#     assert response.status_code == 200
#     assert response.headers["content-type"] == "application/json"

#     data = response.json()
#     assert data == 1


# def test_amy_update_resources():
#     """Test that the /admin/resources/{resource_id} endpoint updates resource content correctly."""
#     response = client.patch("/admin/resources/exam-solutions", json="Hello")

#     assert response.status_code == 200
#     assert response.headers["content-type"] == "application/json"

#     data = response.json()
#     assert data["id"] == "exam-solutions"
#     assert data["content"] == "Hello"


# def test_amy_delete_resources():
#     """Test that the /admin/resources/{resource_id} endpoint deletes resource content correctly."""
#     response = client.post(
#         "/create-text",
#         json={
#             "id": "",
#             "content": "Delete this immediately",
#             "vanity_url": "inappropriate-content",
#             "type": "text",
#             "expiration_time": -1,
#         },
#     )
#     response = client.delete("/admin/resources/inappropriate-content")

#     assert response.status_code == 200
#     assert response.headers["content-type"] == "application/json"

#     data = response.json()
#     assert data["id"] == "inappropriate-content"
#     assert data["content"] == "Delete this immediately"
#     assert data["vanity_url"] == "inappropriate-content"
#     assert data["type"] == "text"

#     response_2 = client.get("/admin/resources")
#     assert len(response_2.json()) == 2
