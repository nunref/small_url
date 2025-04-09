import sqlite3
import datetime

class URLDB:
    def __init__(self, database_name):
        self.database_name = database_name
        self.con = None

        #TODO: move this from here.
        self.connect()
        CREATE_TABLE_SQL = """
            CREATE TABLE IF NOT EXISTS url(
                id INTEGER PRIMARY KEY,
                original_url TEXT NOT NULL,
                short_code TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """
        cur = self.cursor()
        cur.execute(CREATE_TABLE_SQL)
        self.disconnect()

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

