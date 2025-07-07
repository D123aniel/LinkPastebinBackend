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
    con: sqlite3.Connection
    cur: sqlite3.Cursor
    db_service: DatabaseService
    table_name: str

    def __init__(self, con: sqlite3.Connection, cur: sqlite3.Cursor, table_name):
        self.con = con
        self.cur = cur
        self.db_service = DatabaseService(con, cur, table_name)
        self.table_name = table_name

    def generate_random_id(self):
        return "".join(
            random.choices(string.ascii_letters + string.digits, k=random.randint(5, 9))
        )

    # Fix vanity URL
    # If no vanity-url, generate random id
    def create_resource_text(self, resource: Resource) -> Resource:
        # Vanity url present, set as id
        if resource.vanity_url:
            if (
                self.cur.execute(
                    f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE vanity_url=?)",
                    (resource.vanity_url,),
                ).fetchone()[0]
                == 1
            ):
                raise ResourceAlreadyExistsError
            resource.id = resource.vanity_url
        # No vanity url/id, generate a unique id for the resource
        else:
            while not resource.id:
                generated_id = self.generate_random_id()
                if (
                    self.cur.execute(
                        f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE vanity_url=?)",
                        (generated_id,),
                    ).fetchone()[0]
                    == 0
                ):
                    resource.id = generated_id
        # Check once more in case
        if (
            self.cur.execute(
                f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE vanity_url=?)",
                (resource.vanity_url,),
            ).fetchone()[0]
            == 1
        ):
            raise ResourceAlreadyExistsError
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
        if resource.vanity_url:
            if (
                self.cur.execute(
                    f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE vanity_url=?)",
                    (resource.vanity_url,),
                ).fetchone()[0]
                == 1
            ):
                raise ResourceAlreadyExistsError
            resource.id = resource.vanity_url
        # No vanity url/id, generate a unique id for the resource
        else:
            while not resource.id:
                generated_id = self.generate_random_id()
                if (
                    self.cur.execute(
                        f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE vanity_url=?)",
                        (generated_id,),
                    ).fetchone()[0]
                    == 0
                ):
                    resource.id = generated_id
        # Check once more in case
        if (
            self.cur.execute(
                f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE vanity_url=?)",
                (resource.vanity_url,),
            ).fetchone()[0]
            == 1
        ):
            raise ResourceAlreadyExistsError
        resource.type = Type.url
        if resource.expiration_time:
            if isinstance(resource.expiration_time, int):
                resource.expiration_time = datetime.now() + timedelta(
                    hours=resource.expiration_time
                )
        self.db_service.add_entry(resource)
        return resource

    # add redirect stuff here, fastapi can be in services````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
    def get_resource(self, id: str):
        if (
            self.cur.execute(
                f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE id=?)",
                (id,),
            ).fetchone()[0]
            == 0
        ):
            raise ResourceNotFoundError
        self.db_service.update_access_count(id)  # Increment access count
        resource = self.db_service.get_entry(id)

        if resource.type == Type.url:
            return RedirectResponse(url=resource.content)
        else:
            return resource.content

    def get_all_resources(self, type, sort) -> list[Resource]:  # Issue? not sure...
        if type == None and sort == None:  # Return all resources
            return self.db_service.get_all_entries()
        elif type != None and sort == None:  # Filter by type
            selected = self.cur.execute(
                f"SELECT * FROM {self.table_name} WHERE type = ?", (type,)
            ).fetchall()
            output = list()
            for resource_tuple in selected:
                output.append(self.db_service.tuple_to_resource(resource_tuple))
            return output
        elif type == None and sort != None:  # Filter by sort
            output = list()
            selected = self.cur.execute(
                f"SELECT * FROM {self.table_name} WHERE access_count >= ?", (sort,)
            ).fetchall()
            for resource_tuple in selected:
                output.append(self.db_service.tuple_to_resource(resource_tuple))
            return output
        else:  # Filter by type and sort
            output = list()
            selected = self.cur.execute(
                f"SELECT * FROM {self.table_name} WHERE type = ? AND access_count >= ?",
                (type, sort),
            ).fetchall()
            for resource_tuple in selected:
                output.append(self.db_service.tuple_to_resource(resource_tuple))
            return output

    def get_resource_access_count(self, resource_id: str) -> int:
        if (
            self.cur.execute(
                f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE id=?)",
                (resource_id,),
            ).fetchone()[0]
            == 0
        ):
            raise ResourceNotFoundError
        return self.db_service.get_entry(resource_id).access_count

    def update_resource(self, resource_id: str, new_content: str):
        if (
            self.cur.execute(
                f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE id=?)",
                (resource_id,),
            ).fetchone()[0]
            == 0
        ):
            raise ResourceNotFoundError
        self.db_service.update_entry(resource_id, new_content)
        return self.db_service.get_entry(resource_id)

    def delete_resource(self, resource_id: str) -> Resource:
        if (
            self.cur.execute(
                f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE id=?)",
                (resource_id,),
            ).fetchone()[0]
            == 0
        ):
            raise ResourceNotFoundError
        return self.db_service.delete_entry(resource_id)
