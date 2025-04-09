import sqlite3
import datetime
import click
from flask import current_app, g

DATABASE_NAME = "small_url.db"

class URLDB:
    def __init__(self, database_name):
        self.database_name = database_name
        self.con = None

    def connect(self):
        self.con = sqlite3.connect(self.database_name)

    def disconnect(self):
        self.con.close()

    def cursor(self):
        return self.con.cursor()

    def commit(self):
        self.con.commit()

    def insert_url(self, original_url, short_code):
        SQL = "insert into url (original_url, short_code, date) values (?, ?, ?);"
        current_time = datetime.datetime.now()
        params = (original_url, short_code, current_time.isoformat())

        cur = self.cursor()
        cur.execute(SQL, params)
        cur.close()

        self.commit()

    def get_url(self, short_code):
        SQL = "select original_url, short_code, date from url where short_code = ?;"
        params = (short_code,)

        cur = self.cursor()
        res = cur.execute(SQL, params).fetchone()
        cur.close()

        self.close()
        return (res[0], res[1], datetime.datetime.fromisoformat(res[2]))

    def get_many_urls(self, urls_number=5):
        SQL = "select original_url, short_code from url order by date desc limit ?;"
        params = (urls_number,)

        cur = self.cursor()
        res = cur.execute(SQL, params).fetchall()
        cur.close()

        return res

def get_db():
    if "db" not in g:
        g.db = URLDB(DATABASE_NAME)
        g.db.connect()

    return g.db

def close_db(e = None):
    db = g.pop("db", None)

    if db is not None:
        db.disconnect()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def init_db():
    DROP_TABLE_SQL = "DROP TABLE IF EXISTS url;"
    CREATE_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS url(
            id INTEGER PRIMARY KEY,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """
    urldb = URLDB(DATABASE_NAME)
    urldb.connect()
    cur = urldb.cursor()
    cur.execute(DROP_TABLE_SQL)
    cur.execute(CREATE_TABLE_SQL)
    cur.close()
    urldb.disconnect()

@click.command("init-db")
def init_db_command():
    click.echo("Initializing the database ...")
    init_db()
    click.echo("Database initialized")
