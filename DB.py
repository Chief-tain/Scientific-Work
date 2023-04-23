import sqlite3


class DB:

    def __init__(self):
        self.conn = sqlite3.connect('tg_data.db')
        self.cur = self.conn.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS tg_data(
           tg_data_id INTEGER PRIMARY KEY,
           MESSAGE_ID INTEGER,
           SENDER CHAR(255),
           CHAT_TITLE CHAR(255),
           DATE INTEGER,
           MESSAGE TEXT);
        """)
        self.conn.commit()

    def db_cleaning(self):
        try:
            self.cur.execute("""DELETE FROM tg_data;""")
            self.conn.commit()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def insert_into_db(self, new_line):
        self.cur.execute("INSERT INTO tg_data VALUES(NULL, ?, ?, ?, ?, ?);", new_line)
        self.conn.commit()

    def last_date(self):
        self.cur.execute("SELECT MAX(DATE) from tg_data;")
        last_date = self.cur.fetchone()
        return last_date[0]

    def read_db(self, begin, end):
        sqlite_connection = None
        result = []

        try:
            sqlite_connection = sqlite3.connect('tg_data.db')
            cursor = sqlite_connection.cursor()

            cursor.execute("SELECT * from tg_data WHERE DATE BETWEEN ? AND ?", (begin, end))
            records = cursor.fetchall()
            # print(len(records))
            # print(records[0])

            for row in records:
                result.append(
                    {"MESSAGE_ID": row[1], "SENDER": row[2], "CHAT_TITLE": row[3], "DATA": row[4], "MESSAGE": row[5]})

            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                return result
