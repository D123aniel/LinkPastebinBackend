# Script for SQLite3 database creation. Runs on startup

import sqlite3
from models import Resource, Type
from database_startup import db_session
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from resource_entity import ResourceEntity

# Go back and do error handling for all of methods


class DatabaseService:
    __session: Session

    def __init__(self, session: Annotated[Session, Depends(db_session)]):
        self.__session = session

    def add_entry(self, resource: Resource) -> None:
        entry = ResourceEntity.from_model(resource)
        # Check if the resource already exists
        if self.__session.query(ResourceEntity).filter_by(id=resource.id).count() == 0:
            self.__session.add(entry)
        else:
            raise ValueError(f"Resource with id {resource.id} already exists.")
        self.__session.commit()

    def get_entry(self, id: str) -> Resource:
        resource = self.__session.query(ResourceEntity).filter_by(id=id).first()
        return resource

    def filter_by(self, **kwargs) -> list[Resource]:
        # Print the arguments passed
        print(
            "````````````````````````````````````Filtering by:",
            kwargs,
            "````````````````````````````````````",
        )
        query = self.__session.query(ResourceEntity)

        for key, value in kwargs.items():
            if key == "type":
                query = query.filter_by(type=value)
            if isinstance(value, tuple) and len(value) == 2:
                operator, operand = value
                print(key, " ", operator, " ", operand)
                if operator is None or operand is None:
                    continue
                if operator == "=":
                    query = query.filter(ResourceEntity.access_count == operand)
                elif operator == "<":
                    query = query.filter(ResourceEntity.access_count < operand)
                elif operator == ">":
                    query = query.filter(ResourceEntity.access_count > operand)
                elif operator == "<=":
                    query = query.filter(ResourceEntity.access_count <= operand)
                elif operator == ">=":
                    query = query.filter(ResourceEntity.access_count >= operand)
                else:
                    raise ValueError(f"Unsupported operator: {operator}")
        # All Query entries should be made to go from Resource to ResourceEntity
        query_result = query.all()
        return [entity.to_model() for entity in query_result]

    def resource_exists(self, **kwargs) -> bool:
        queried = self.filter_by(**kwargs)
        return len(queried) > 0

    def get_all_entries(self) -> list[Resource]:
        resources = self.__session.query(ResourceEntity).all()
        return [entity.to_model() for entity in resources]

    def update_entry(self, id: str, content: str) -> None:
        resource_entity = self.__session.query(ResourceEntity).filter_by(id=id).first()
        if resource_entity is None:
            raise ValueError(f"Resource with id {id} not found.")
        resource_entity.content = content
        self.__session.commit()

    def update_access_count(self, id: str) -> None:
        resource_entity = self.__session.query(ResourceEntity).filter_by(id=id).first()
        if resource_entity is None:
            raise ValueError(f"Resource with id {id} not found.")
        resource_entity.access_count += 1
        self.__session.commit()

    def delete_entry(self, id: str) -> Resource:
        resource_entity = self.__session.query(ResourceEntity).filter_by(id=id).first()
        if resource_entity is None:
            raise ValueError(f"Resource with id {id} not found.")
        self.__session.delete(resource_entity)
        self.__session.commit()
        return resource_entity.to_model()

    def delete_all_entries(self) -> None:
        self.__session.query(ResourceEntity).delete()
        self.__session.commit()

    def tuple_to_resource(self, resource_tuple) -> Resource:
        return Resource(
            id=resource_tuple[0],
            content=resource_tuple[1],
            vanity_url=resource_tuple[2],
            type=Type(resource_tuple[3]),
            expiration_time=resource_tuple[4],
            access_count=resource_tuple[5],
        )
