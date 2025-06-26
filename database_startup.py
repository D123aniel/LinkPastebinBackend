# This script initializes a SQLite database for storing paste data. Run on docker container startup

import sqlite3

con = sqlite3.connect("paste-link.db")

cur = con.cursor()  # Create a cursor object to execute SQL commands with Python

cur.execute(
    "CREATE TABLE IF NOT EXISTS pastes(id TEXT PRIMARY KEY, content TEXT, vanity_url TEXT, type TEXT, expiration_time INTEGER, access_count INTEGER)"
)  # Name of the table is pastes
