import string
from models import Resource, Type
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
from pydantic import Field, BaseModel
from enum import Enum
from typing import Annotated, TypeAlias

import random

# This is where actual functionality of the service is implemented

resource_db = {}


class ResourceAlreadyExistsError(Exception):
    """Exception raised when resource already exists"""

    pass


class ResourceNotFoundError(Exception):
    """Exception raised when resource not found"""

    pass


class ResourceServices:

    def generate_random_id(self):
        return "".join(
            random.choices(string.ascii_letters + string.digits, k=random.randint(5, 9))
        )

    # Fix vanity URL
    # If no vanity-url, generate random id
    def create_resource_text(self, resource: Resource) -> Resource:
        # Vanity url present, set as id
        if resource.vanity_url:
            if resource.vanity_url in resource_db:
                raise ResourceAlreadyExistsError
            resource.id = resource.vanity_url
        # No vanity url/id, generate a unique id for the resource
        else:
            while not resource.id:
                generated_id = self.generate_random_id()
                if generated_id not in resource_db:
                    resource.id = generated_id
        # Check once more in case
        if resource.id in resource_db:
            raise ResourceAlreadyExistsError
        resource.type = Type.text
        # Expiration date handling
        if resource.expiration_time:
            if isinstance(resource.expiration_time, int):
                if resource.expiration_time >= 0:
                    resource.expiration_time = datetime.now() + timedelta(
                        hours=resource.expiration_time
                    )
        resource_db[resource.id] = resource
        return resource

    def create_resource_url(self, resource: Resource) -> Resource:
        if resource.vanity_url:
            if resource.vanity_url in resource_db:
                raise ResourceAlreadyExistsError
            resource.id = resource.vanity_url
        else:
            while not resource.id:
                generated_id = self.generate_random_id()
                if generated_id not in resource_db:
                    resource.id = generated_id
        if resource.id in resource_db:
            raise ResourceAlreadyExistsError
        resource.type = Type.url
        if resource.expiration_time:
            if isinstance(resource.expiration_time, int):
                resource.expiration_time = datetime.now() + timedelta(
                    hours=resource.expiration_time
                )
        resource_db[resource.id] = resource
        return resource

    # add redirect stuff here, fastapi can be in services````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
    def get_resource(self, id: str):
        if id not in resource_db:
            raise ResourceNotFoundError
        resource = resource_db[id]
        resource.access_count += 1

        if resource.type == Type.url:
            return RedirectResponse(url=resource.content)
        else:
            return resource.content

    def get_all_resources(self, type, sort) -> list[Resource]:
        if type == None and sort == None:
            return list(resource_db.values())
        elif type != None and sort == None:
            output = list()
            for resource_id in resource_db:
                if type == "text":
                    if resource_db[resource_id].type == Type.text:
                        output.append(resource_db[resource_id])
                else:
                    if resource_db[resource_id].type == Type.url:
                        output.append(resource_db[resource_id])
            return output
        elif type == None and sort != None:
            output = list()
            for resource_id in resource_db:
                if resource_db[resource_id].access_count >= sort:
                    output.append(resource_db[resource_id])
            return output
        else:
            output = list()
            for resource_id in resource_db:
                if type == "text":
                    if (
                        resource_db[resource_id].type == Type.text
                        and resource_db[resource_id].access_count >= sort
                    ):
                        output.append(resource_db[resource_id])
                else:
                    if (
                        resource_db[resource_id].type == Type.url
                        and resource_db[resource_id].access_count >= sort
                    ):
                        output.append(resource_db[resource_id])
            return output

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
