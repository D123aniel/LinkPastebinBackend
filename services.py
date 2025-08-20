import string
from models import Resource, Type
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
from pydantic import Field, BaseModel
from enum import Enum
from typing import Annotated, TypeAlias
import sqlite3
from database import DatabaseService


import random

# This is where actual functionality of the service is implemented


class ResourceAlreadyExistsError(Exception):
    """Exception raised when resource already exists"""

    pass


class ResourceNotFoundError(Exception):
    """Exception raised when resource not found"""

    pass


class ResourceServices:
    db_service: DatabaseService

    def __init__(self):
        self.db_service = DatabaseService()

    def generate_random_id(self):
        return "".join(
            random.choices(string.ascii_letters + string.digits, k=random.randint(5, 9))
        )

    # Fix vanity URL
    # If no vanity-url, generate random id
    def create_resource_text(self, resource: Resource) -> Resource:
        # Check for existing id
        if self.db_service.get_entry(resource.id):
            raise ResourceAlreadyExistsError

        # Vanity url present, set as id
        if resource.vanity_url and resource.vanity_url.strip() != "":
            if self.db_service.resource_exists(
                vanity_url=resource.vanity_url
            ) or self.db_service.resource_exists(id=resource.vanity_url):
                raise ResourceAlreadyExistsError
            resource.id = resource.vanity_url
        # No vanity url/id, generate a unique id for the resource
        else:
            while not resource.id or self.db_service.resource_exists(
                vanity_url=resource.id
            ):
                generated_id = self.generate_random_id()
                if self.db_service.resource_exists(vanity_url=generated_id) == False:
                    resource.id = generated_id
        resource.type = Type.text
        # Expiration date handling
        if resource.expiration_time:
            if isinstance(resource.expiration_time, int):
                if resource.expiration_time >= 0:
                    resource.expiration_time = datetime.now() + timedelta(
                        hours=resource.expiration_time
                    )
        self.db_service.add_entry(resource)
        return resource

    def create_resource_url(self, resource: Resource) -> Resource:
        # Check for existing id
        if self.db_service.get_entry(resource.id):
            raise ResourceAlreadyExistsError

        # Vanity url present, set as id
        if resource.vanity_url and resource.vanity_url.strip() != "":
            if self.db_service.resource_exists(
                vanity_url=resource.vanity_url
            ) or self.db_service.resource_exists(id=resource.vanity_url):
                raise ResourceAlreadyExistsError
            resource.id = resource.vanity_url
        # No vanity url/id, generate a unique id for the resource
        else:
            while not resource.id or self.db_service.resource_exists(
                vanity_url=resource.id
            ):
                generated_id = self.generate_random_id()
                if self.db_service.resource_exists(vanity_url=generated_id) == False:
                    resource.id = generated_id
        resource.type = Type.url
        # Expiration date handling
        if resource.expiration_time:
            if isinstance(resource.expiration_time, int):
                if resource.expiration_time >= 0:
                    resource.expiration_time = datetime.now() + timedelta(
                        hours=resource.expiration_time
                    )
        self.db_service.add_entry(resource)
        return resource

    def get_resource(self, id: str):
        if not self.db_service.resource_exists(id=id):
            raise ResourceNotFoundError
        self.db_service.update_access_count(id)  # Increment access count
        resource = self.db_service.get_entry(id)

        if resource.type == Type.url:
            return RedirectResponse(url=resource.content)
        else:
            return resource.content

    def get_all_resources(
        self, type: Type, sort_operator: str, sort_value: int
    ) -> list[Resource]:  # Issue? not sure...
        if (
            type == None and sort_operator == None and sort_value == None
        ):  # Return all resources
            return self.db_service.get_all_entries()

        selected = self.db_service.filter_by(
            type=type, sort=(sort_operator, sort_value)
        )
        out = list()
        for resource_tuple in selected:
            out.append(self.db_service.tuple_to_resource(resource_tuple))
        return out

    def get_resource_access_count(self, resource_id: str) -> int:
        if not self.db_service.resource_exists(id=resource_id):
            raise ResourceNotFoundError
        return self.db_service.get_entry(resource_id).access_count

    def update_resource(self, resource_id: str, new_content: str):
        if not self.db_service.resource_exists(id=resource_id):
            raise ResourceNotFoundError
        self.db_service.update_entry(resource_id, new_content)
        return self.db_service.get_entry(resource_id)

    def delete_resource(self, resource_id: str) -> Resource:
        if not self.db_service.resource_exists(id=resource_id):
            raise ResourceNotFoundError
        return self.db_service.delete_entry(resource_id)

    def delete_all_resources(self):
        self.db_service.delete_all_entries()
        return True
