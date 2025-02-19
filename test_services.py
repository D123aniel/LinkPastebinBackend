from unittest.mock import MagicMock
from services import ResourceServices, resource_db
from models import Resource, Type
from datetime import datetime, UTC
from fastapi.responses import RedirectResponse


def test_get_all_resources():
    service = ResourceServices()
    resource1 = Resource(id="id1", content="Content 1", type=Type.text)
    resource2 = Resource(id="id2", content="Content 2", type=Type.url)
    resource_db["id1"] = resource1
    resource_db["id2"] = resource2

    all_resources = service.get_all_resources()

    assert (
        len(all_resources) == 4
    )  # 2 for the new resources we created, 2 for exam-solutions and test-solutions
    assert resource1 in all_resources
    assert resource2 in all_resources


def test_random_id_creation():
    service = ResourceServices()
    resource = Resource(id="", content="Foo Bar", type=Type.text)

    created_resource = service.create_resource_text(resource)

    assert created_resource.id != ""
    assert created_resource.id != None
    assert len(created_resource.id) >= 1
    assert created_resource.content == "Foo Bar"
    assert created_resource.type == Type.text


def test_create_resource_text():
    service = ResourceServices()
    resource = Resource(id="mock_id", content="Sample text", type=Type.text)

    created_resource = service.create_resource_text(resource)

    assert created_resource.id == "mock_id"
    assert created_resource.content == "Sample text"
    assert created_resource.type == Type.text
    assert created_resource.id in resource_db


def test_create_resource_url():
    service = ResourceServices()
    resource = Resource(
        id="mock_id_2",
        content="https://fastapi.tiangolo.com/reference/parameters/?h=path%28#fastapi.Query",
        type=Type.url,
    )

    created_resource = service.create_resource_url(resource)

    assert created_resource.id == "mock_id_2"
    assert created_resource.type == Type.url
    assert (
        created_resource.content
        == "https://fastapi.tiangolo.com/reference/parameters/?h=path%28#fastapi.Query"
    )
    assert created_resource.id in resource_db


def test_get_resource():
    service = ResourceServices()
    resource = Resource(id="test_id", content="Test content", type=Type.text)
    resource_db["test_id"] = resource

    content = service.get_resource("test_id")

    assert content == "Test content"

    resource_2 = Resource(
        id="real-test-solutions",
        content="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        type=Type.url,
    )
    resource_db["real-test-solutions"] = resource_2

    content = service.get_resource("real-test-solutions")

    assert content.status_code == 307
    assert content.headers["location"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert isinstance(content, RedirectResponse)


def test_get_resource_access_count():
    service = ResourceServices()
    resource = Resource(id="test_id", content="Test content", type=Type.text)
    resource_db["test_id"] = resource

    access_count = service.get_resource_access_count("test_id")

    assert access_count == 0

    service.get_resource("test_id")

    new_access_count = service.get_resource_access_count("test_id")
    assert new_access_count == 1


def test_update_resource():
    service = ResourceServices()
    resource = Resource(id="test_id", content="Old content", type=Type.text)
    resource_db["test_id"] = resource

    updated_resource = service.update_resource("test_id", "Updated content")

    assert updated_resource.content == "Updated content"


def test_delete_resource():
    service = ResourceServices()
    resource = Resource(id="test_id", content="Test content", type=Type.text)
    resource_db["test_id"] = resource

    deleted_resource = service.delete_resource("test_id")

    assert deleted_resource.content == "Test content"
    assert "test_id" not in resource_db
