import sqlite3
import datetime

class URLDB:
    def __init__(self, database_name):
        self.database_name = database_name

    def insert_url(self, original_url, short_code):
        SQL = "insert into url (original_url, short_code, date) values (?, ?, ?);"
        current_time = datetime.datetime.now()
        params = (original_url, short_code, current_time.isoformat())

        con = sqlite3.connect(self.database_name)
        cur = con.cursor()
        cur.execute(SQL, params)
        con.commit()

        cur.close()
        con.close()

    def get_url(self, short_code):
        SQL = "select original_url, short_code, date from url where short_code = ?;"
        params = (short_code,)

        con = sqlite3.connect(self.database_name)
        cur = con.cursor()
        res = cur.execute(SQL, params).fetchone()

        cur.close()
        con.close()
        print(res)
        return (res[0], res[1], datetime.datetime.fromisoformat(res[2]))

    def get_all_url(self):
        pass
