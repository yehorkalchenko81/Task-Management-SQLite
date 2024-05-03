import sqlite3 as sq


def create_table(path: str = './database.db'):
    with sq.connect(path) as conn:
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                fullname VARCHAR(100),
                email VARCHAR(100) UNIQUE
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS status (
                id INTEGER PRIMARY KEY,
                name VARCHAR(50) UNIQUE
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title VARCHAR(100),
                description VARCHAR(100),
                status_id INTEGER,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (status_id) REFERENCES status (id)
            )
        ''')

        conn.commit()


if __name__ == '__main__':
    create_table()
