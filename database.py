# Script for SQLite3 database creation. Runs on startup

import sqlite3
from models import Resource, Type
from database_startup import db_session
from fastapi import Depends
from sqlalchemy.orm import Session

# Go back and do error handling for all of methods


class DatabaseService:

    def __init__(self, session: Session = Depends(db_session)):
        self.__session = session

    def add_entry(self, resource: Resource) -> None:
        # Check if the resource already exists
        if self.__session.query(Resource).filter_by(id=resource.id).count() == 0:
            self.__session.add(resource)
        else:
            raise ValueError(f"Resource with id {resource.id} already exists.")
        self.__session.commit()

    def get_entry(self, id: str) -> Resource | None:
        resource = self.__session.query(Resource).filter_by(id=id).first()
        if resource is None:
            raise ValueError(f"Resource with id {id} not found.")
        return resource

    def get_all_entries(self) -> list[Resource]:
        self.cur.execute(f"SELECT * FROM {self.table_name}")
        return [self.tuple_to_resource(row) for row in self.cur.fetchall()]

    def update_entry(self, id: str, content: str) -> None:
        self.cur.execute(
            f"UPDATE {self.table_name} SET content = ? WHERE id = ?",
            (
                content,
                id,
            ),
        )
        self.con.commit()

    def update_access_count(self, id: str) -> None:
        self.cur.execute(
            f"UPDATE {self.table_name} SET access_count = access_count + 1 WHERE id = ?",
            (id,),
        )
        self.con.commit()

    def delete_entry(self, id: str) -> Resource:
        resource = self.get_entry(id)
        self.cur.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (id,))
        self.con.commit()
        return resource

    def delete_all_entries(self) -> None:
        self.cur.execute(f"DELETE FROM {self.table_name}")
        self.con.commit()

    def tuple_to_resource(self, resource_tuple) -> Resource:
        return Resource(
            id=resource_tuple[0],
            content=resource_tuple[1],
            vanity_url=resource_tuple[2],
            type=Type(resource_tuple[3]),
            expiration_time=resource_tuple[4],
            access_count=resource_tuple[5],
        )
