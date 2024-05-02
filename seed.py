import sqlite3
import faker
from random import randint


def fake_users(users_data):
    fake_users_data = []
    fake_data = faker.Faker()

    for _ in range(users_data):
        fullname = fake_data.name()
        email = fake_data.email()
        fake_users_data.append((fullname, email))

    return fake_users_data


def generate_fake_data(fa_data):
    fake_data = faker.Faker()
    fakes_data = []

    for i in range(fa_data):
        f_title = fake_data.sentence()
        f_description = fake_data.text()
        f_status_id = randint(1, 3)
        f_user_id = randint(1, 10)
        fakes_data.append((f_title, f_description, f_status_id, f_user_id))

    return fakes_data


def insert_data_to_db(fakes_data, uf_data) -> None:
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()

        user_data = '''INSERT INTO users (fullname, email) VALUES (?,?) '''
        cur.executemany(user_data, uf_data)

        inserting = """INSERT INTO tasks (title,description,status_id,user_id) VALUES (?,?,?,?)"""
        cur.executemany(inserting, fakes_data)

        conn.commit()


if __name__ == "__main__":
    fa_data = 20
    users_data = 20

    uf_data = fake_users(users_data)
    f_data = generate_fake_data(fa_data)

    insert_data_to_db(f_data, uf_data)
