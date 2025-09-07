from unittest.mock import MagicMock
from services import ResourceServices
from models import Resource, Type
import sqlite3
from database import DatabaseService
from datetime import datetime, UTC
from fastapi.responses import RedirectResponse


# def global_setup():
#     global connect, curs, db_service, service
#     connect = sqlite3.connect("test.db", check_same_thread=False)
#     curs = connect.cursor()
#     curs.execute("DROP TABLE IF EXISTS test")
#     curs.execute(
#         "CREATE TABLE test(id, content, vanity_url, type, expiration_time, access_count)"
#     )
#     db_service = DatabaseService(connect, curs, "test")
#     service = ResourceServices(connect, curs, "test")
#     connect.commit()


# global_setup()


# def test_get_all_resources():
#     resource1 = Resource(id="id1", content="Content 1", type=Type.text)
#     resource2 = Resource(id="id2", content="Content 2", type=Type.url)
#     db_service.add_entry(resource1)
#     db_service.add_entry(resource2)

#     all_resources = service.get_all_resources(None, None)

#     assert len(all_resources) == 2  # 2 for the new resources we created
#     assert resource1 in all_resources
#     assert resource2 in all_resources


# def test_get_all_resources_queried():
#     service = ResourceServices(connect, curs, "test")

#     service.get_resource("id1")  # access_count = 1
#     service.get_resource("id1")  # access_count = 2
#     service.get_resource("id1")  # access_count = 3
#     service.get_resource("id2")  # access_count = 1
#     service.get_resource("id2")  # access_count = 2
#     service.get_resource("id2")  # access_count = 3
#     service.get_resource("id2")  # access_count = 4
#     # Print access counts for debugging
#     print(f"Resource id1 access count: {service.get_resource_access_count('id1')}")
#     print(f"Resource id2 access count: {service.get_resource_access_count('id2')}")

#     # Type filter no sort
#     links = service.get_all_resources("link", None)  # Should return id_2
#     assert len(links) == 1
#     assert links[0].id == "id2"

#     # Sort filter no type
#     viewed = service.get_all_resources(None, 2)  # Should return id1 and id2
#     assert len(viewed) == 2
#     assert viewed[0].id == "id1"
#     assert viewed[1].id == "id2"

#     # Type and Sort
#     viewed_links = service.get_all_resources("link", 2)  # Should only return id2
#     assert len(viewed_links) == 1
#     assert viewed_links[0].id == "id2"


# def test_random_id_creation():
#     resource = Resource(id="", content="Foo Bar", type=Type.text)

#     created_resource = service.create_resource_text(resource)

#     assert created_resource.id != ""
#     assert created_resource.id != None
#     assert len(created_resource.id) >= 1
#     assert created_resource.content == "Foo Bar"
#     assert created_resource.type == Type.text


# def test_create_resource_text():
#     resource = Resource(id="mock_id", content="Sample text", type=Type.text)

#     created_resource = service.create_resource_text(resource)

#     assert created_resource.id == "mock_id"
#     assert created_resource.content == "Sample text"
#     assert created_resource.type == Type.text
#     all_ids = [r.id for r in db_service.get_all_entries()]
#     assert created_resource.id in all_ids


# def test_create_resource_url():
#     resource = Resource(
#         id="mock_id_2",
#         content="https://fastapi.tiangolo.com/reference/parameters/?h=path%28#fastapi.Query",
#         type=Type.url,
#     )

#     created_resource = service.create_resource_url(resource)

#     assert created_resource.id == "mock_id_2"
#     assert created_resource.type == Type.url
#     assert (
#         created_resource.content
#         == "https://fastapi.tiangolo.com/reference/parameters/?h=path%28#fastapi.Query"
#     )
#     all_ids = [r.id for r in db_service.get_all_entries()]
#     assert created_resource.id in all_ids


# def test_get_resource():
#     resource = Resource(id="test_id", content="Test content", type=Type.text)
#     service.create_resource_text(resource)

#     content = service.get_resource("test_id")

#     assert content == "Test content"

#     resource_2 = Resource(
#         id="real-test-solutions",
#         content="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
#         type=Type.url,
#     )
#     service.create_resource_url(resource_2)

#     content = service.get_resource("real-test-solutions")

#     assert isinstance(content, RedirectResponse)
#     assert content.status_code == 307
#     assert content.headers["location"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


# def test_get_resource_access_count():
#     resource = Resource(id="test_id_2", content="Test content", type=Type.text)
#     service.create_resource_text(resource)

#     access_count = service.get_resource_access_count("test_id_2")

#     assert access_count == 0

#     service.get_resource("test_id_2")

#     new_access_count = service.get_resource_access_count("test_id_2")
#     assert new_access_count == 1


# def test_update_resource():
#     resource = Resource(id="test_id_3", content="Old content", type=Type.text)
#     service.create_resource_text(resource)

#     assert resource.content == "Old content"

#     updated_resource = service.update_resource("test_id_3", "Updated content")

#     assert updated_resource.content == "Updated content"


# def test_delete_resource():
#     resource = Resource(id="test_id_4", content="Test content", type=Type.text)
#     service.create_resource_text(resource)

#     deleted_resource = service.delete_resource("test_id_4")

#     assert deleted_resource.content == "Test content"
#     all_ids = [r.id for r in db_service.get_all_entries()]
#     assert deleted_resource.id not in all_ids
