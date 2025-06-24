import sqlite3

con = sqlite3.connect("paste-link.db")

cur = con.cursor()  # Create a cursor object to execute SQL commands with Python

cur.execute(
    "CREATE TABLE IF NOT EXISTS pastes(id, content, vanity_url, type, expiration_time, access_count)"
)  # Name of the table is pastes

res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchone())
