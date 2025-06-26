# Script for SQLite3 database creation. Runs on startup

import sqlite3
from models import Resource, Type

# Go back and do error handling for all of methods


class DatabaseService:
    con: sqlite3.Connection
    cur: sqlite3.Cursor

    def __init__(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor):
        self.con = connection
        self.cur = cursor

    def add_entry(self, resource: Resource):
        self.cur.execute(
            "INSERT INTO pastes VALUES (?, ?, ?, ?, ?, ?)",
            (
                resource.id,
                resource.content,
                resource.vanity_url,
                resource.type.value,
                resource.expiration_time,
                resource.access_count,
            ),
        )
        self.con.commit()

    def get_entry(self, id: str) -> Resource:
        self.cur.execute("SELECT * FROM pastes WHERE id = ?", (id,))
        return self.tuple_to_resource(self.cur.fetchone())

    def get_all_entries(self):
        self.cur.execute("SELECT * FROM pastes")
        return self.cur.fetchall()

    def update_entry(self, id: str, content: str):
        self.cur.execute(
            "UPDATE pastes SET content = ? WHERE id = ?",
            (
                content,
                id,
            ),
        )
        self.con.commit()

    def delete_entry(self, id: str) -> Resource:
        resource = self.get_entry(id)
        self.cur.execute("DELETE FROM pastes WHERE id = ?", (id,))
        self.con.commit()
        return resource

    def tuple_to_resource(self, resource_tuple) -> Resource:
        return Resource(
            id=resource_tuple[0],
            content=resource_tuple[1],
            vanity_url=resource_tuple[2],
            type=Type(resource_tuple[3]),
            expiration_time=resource_tuple[4],
            access_count=resource_tuple[5],
        )
