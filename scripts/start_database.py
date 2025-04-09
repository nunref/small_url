import sqlite3

CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS url(
        id INTEGER PRIMARY KEY,
        original_url TEXT NOT NULL,
        short_code TEXT NOT NULL,
        date TEXT NOT NULL
    )
"""

print("Creating the database")
con = sqlite3.connect("small_url.db")
cur = con.cursor()
cur.execute(CREATE_TABLE_SQL)
print("Ok")

