import sqlite3

con = sqlite3.connect("paste-link.db")

cur = con.cursor()  # Create a cursor object to execute SQL commands with Python

cur.execute(
    "CREATE TABLE IF NOT EXISTS pastes(id, content, vanity_url, type, expiration_time, access_count)"
)  # Name of the table is pastes

from database import DatabaseService

db_service = DatabaseService(con, cur)

# cur.execute("SELECT * FROM pastes")
# print(cur.fetchall())  # Print all entries in the pastes table

# print(type(db_service.get_entry("oqkasl")))  # Print the entry with id "example_id"

# Get list of all ids in the pastes table
cur.execute("SELECT id FROM pastes WHERE type = ?", ("text",))
# print(cur.fetchall())  # Print all entries in the pastes table
# Print all ids in the pastes table
print([row[0] for row in cur.fetchall()])  # Print all ids in the pastes table
