import string
from models import Resource, Type
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
from pydantic import Field, BaseModel
from enum import Enum
from typing import Annotated, TypeAlias
import sqlite3
from database import DatabaseService
from sqlalchemy.orm import Session
from fastapi import Depends


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

    def __init__(self, db_service: Annotated[DatabaseService, Depends()]):
        self.db_service = db_service

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
        # While resource id is empty or vanity_url is resource id, or id is resource id
        # Intially, no resource id or vanity_url
        # Now, we have a generated_id. Check if it already exists
        else:
            while (
                not resource.id
                or self.db_service.resource_exists(vanity_url=resource.id)
                or self.db_service.resource_exists(id=resource.id)
            ):
                generated_id = self.generate_random_id()
                print(
                    f"{self.db_service.resource_exists(
                    vanity_url=generated_id
                )} and {self.db_service.resource_exists(id=generated_id)}"
                )
                if self.db_service.resource_exists(
                    vanity_url=generated_id
                ) == False and not self.db_service.resource_exists(id=generated_id):
                    resource.id = generated_id
                    print("Entered break")
                    break
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
            while (
                not resource.id
                or self.db_service.resource_exists
                or self.db_service.resource_exists(id=resource.id)(
                    vanity_url=resource.id
                )
            ):
                generated_id = self.generate_random_id()
                if self.db_service.resource_exists(
                    vanity_url=generated_id
                ) == False and not self.db_service.resource_exists(id=generated_id):
                    resource.id = generated_id
                    break
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
        if resource is None:
            raise ValueError("Resource doesn't exist")

        if resource.type == Type.url:
            return RedirectResponse(url=resource.content)
        else:
            return resource.content

    def get_all_resources(
        self,
        resource_type: Type | None,
        sort_operator: str | None,
        sort_value: int | None,
    ) -> list[Resource]:  # Issue? not sure...
        if (
            resource_type == None and sort_operator == None and sort_value == None
        ):  # Return all resources
            return self.db_service.get_all_entries()
        out = list()
        if resource_type is None:
            selected_link = self.db_service.filter_by(
                type=Type.url, sort=(sort_operator, sort_value)
            )
            selected_text = self.db_service.filter_by(
                type=Type.text, sort=(sort_operator, sort_value)
            )
            out = selected_link + selected_text
            print("out type: ", type(out))
        else:
            selected = self.db_service.filter_by(
                type=resource_type, sort=(sort_operator, sort_value)
            )
            print("selected type: ", type(selected))
            for resource_tuple in selected:
                out.append(resource_tuple)
            print("type: ", type(out))
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
