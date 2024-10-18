import sqlite3


class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS survey_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    gender TEXT,
                    tg_id INTEGER,
                    genre TEXT
                )
            """)

            connection.commit()

    def execute(self, query: str, params: tuple = None):
        with sqlite3.connect(self.path) as connection:
            connection.execute(query, params)
            connection.commit()