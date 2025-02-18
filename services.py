from models import Resource, Type
from datetime import datetime
from pydantic import Field, BaseModel
from enum import Enum
from typing import Annotated, TypeAlias


# This is where actual functionality of the service is implemented

resource_db = {}


class ResourceAlreadyExistsError(Exception):
    """Exception raised when resource already exists"""

    pass


class ResourceNotFoundError(Exception):
    """Exception raised when resource not found"""

    pass


class ResourceServices:

    # If no vanity-url, generate random id
    def create_resource_text(self, resource: Resource) -> Resource:
        if resource.id in resource_db:
            raise ResourceAlreadyExistsError
        resource.type = Type.text
        resource_db[resource.id] = resource
        return resource

    def create_resource_url(self, resource: Resource) -> Resource:
        if resource.id in resource_db:
            raise ResourceAlreadyExistsError
        resource.type = Type.url
        resource_db[resource.id] = resource
        return resource

    def get_resource(self, id: str) -> tuple[str, str]:
        if id not in resource_db:
            raise ResourceNotFoundError
        resource = resource_db[id]
        return resource.content, resource.type

    def get_all_resources(self) -> list[Resource]:
        return list(resource_db.values())

    def get_resource_access_count(self, resource_id: str) -> int:
        if resource_id not in resource_db:
            raise ResourceNotFoundError
        return resource_db[resource_id].access_count

    def update_resource(self, resource_id: str, new_content: str):
        if resource_id not in resource_db:
            raise ResourceNotFoundError
        resource_db[resource_id].content = new_content
        return resource_db[resource_id]

    def delete_resource(self, resource_id: str) -> Resource:
        if resource_id not in resource_db:
            raise ResourceNotFoundError
        return resource_db.pop(resource_id)
