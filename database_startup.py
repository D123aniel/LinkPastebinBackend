# This script initializes a SQLite database for storing paste data. Run on docker container startup

import sqlite3

con = sqlite3.connect("paste-link.db", check_same_thread=False)

cur = con.cursor()  # Create a cursor object to execute SQL commands with Python

cur.execute(
    "CREATE TABLE IF NOT EXISTS pastes(id, content, vanity_url, type, expiration_time, access_count)"
)  # Name of the table is pastes
con.commit()

con = sqlite3.connect("test.db", check_same_thread=False)
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS test(id, content, vanity_url, type, expiration_time, access_count)"
)  # Create a test table for user data
con.commit()
