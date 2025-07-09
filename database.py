# Script for SQLite3 database creation. Runs on startup

import sqlite3
from models import Resource, Type

# Go back and do error handling for all of methods


class DatabaseService:
    con: sqlite3.Connection
    cur: sqlite3.Cursor
    table_name: str

    def __init__(
        self, connection: sqlite3.Connection, cursor: sqlite3.Cursor, table_name: str
    ):
        self.con = connection
        self.cur = cursor
        self.table_name = table_name

    def add_entry(self, resource: Resource) -> None:
        # Check if the resource already exists
        if (
            self.cur.execute(
                f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE id=?)",
                (resource.id,),
            ).fetchone()[0]
            == 0
        ):
            self.cur.execute(
                f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?, ?, ?)",
                (
                    resource.id,
                    resource.content,
                    resource.vanity_url,
                    resource.type.value,
                    resource.expiration_time,
                    resource.access_count,
                ),
            )
        else:
            raise ValueError(f"Resource with id {resource.id} already exists.")
        self.con.commit()

    def get_entry(self, id: str) -> Resource:
        self.cur.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (id,))
        return self.tuple_to_resource(self.cur.fetchone())

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
