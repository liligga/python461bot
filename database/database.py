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
            connection.execute("""
                CREATE TABLE IF NOT EXISTS genres (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    author TEXT,
                    price INTEGER,
                    genre_id INTEGER,
                    FOREIGN KEY (genre_id) REFERENCES genres(id)
                )
            """)

            connection.commit()

    def execute(self, query: str, params: tuple = None):
        with sqlite3.connect(self.path) as connection:
            connection.execute(query, params)
            connection.commit()

    def fetch(self, query: str, params: tuple = tuple()):
        with sqlite3.connect(self.path) as conn:
            result = conn.execute(query, params)
            result.row_factory = sqlite3.Row

            data = result.fetchall()
            return [dict(row) for row in data]
