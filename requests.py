import sqlite3 as sq


def call_requests(path: str = './database.db'):
    with sq.connect(path) as conn:
        cur = conn.cursor()

        cur.execute('''
            INSERT INTO status
            VALUES (?, ?),
                   (?, ?),
                   (?, ?)  
        ''',
            (
                1, 'new',
                2, 'in progress',
                3, 'completed'
            )
        )

        cur.execute('''
            INSERT INTO users 
            VALUES (?, ?, ?),
                   (?, ?, ?)
        ''',
            (
                1, 'Yehor Kalchenko', 'example@i.ua',
                2, 'Misha Kalchenko', 'misha@gmail.com'
            )
        )

        cur.execute('''
            INSERT INTO tasks
            VALUES (?, ?, ?, ?, ?)
        ''',
            (1, 'Homework', None, 1, 1)
        )

        # Отримати всі завдання певного користувача
        cur.execute('''
            SELECT * FROM tasks
            WHERE user_id = ?
        ''',
            (1,)
        )

        # Вибрати завдання за певним статусом
        cur.execute('''
            SELECT * FROM tasks 
            WHERE status_id = (
                SELECT id FROM status
                WHERE name = ?
            )
        ''',
            ('new',)
        )

        # Оновити статус конкретного завдання
        cur.execute('''
            UPDATE tasks 
            SET status_id = (
                SELECT id FROM status
                WHERE name = ?
            )
            WHERE ID = ?
        ''',
            ('completed', 1)
        )

        # Отримати список користувачів, які не мають жодного завдання
        cur.execute('''
            SELECT * FROM users 
            WHERE id NOT IN (
                SELECT user_id FROM tasks
            ) 
        ''')

        # Додати нове завдання для конкретного користувача
        cur.execute('''
            INSERT INTO tasks
            VALUES (?, ?, ?, ?, ?),
                   (?, ?, ?, ?, ?)
        ''',
            (
                2, 'Walk a dog', 'Spend 30 minutes by walking', 1, 2,
                3, 'Example', 'Description', 1, 1
             )
        )

        # Отримати всі завдання, які ще не завершено
        cur.execute('''
            SELECT * FROM tasks
            WHERE status_id = (
                SELECT id FROM status
                WHERE name = ?
            )
        ''',
            ('completed',)
        )

        # Видалити конкретне завдання
        cur.execute('''
            DELETE FROM tasks
            WHERE id = ?
        ''',
            (3,)
        )

        # Знайти користувачів з певною електронною поштою
        cur.execute('''
            SELECT * FROM users
            WHERE email LIKE ?
        ''',
            ('misha%',)
        )

        # Оновити ім'я користувача
        cur.execute('''
            UPDATE users
            SET fullname = ?
            WHERE id = ?
        ''',
            ('Mychailo Kalchenko', 2)
        )

        # Отримати кількість завдань для кожного статусу
        cur.execute('''
            SELECT COUNT(status_id) AS total, status_id
            FROM tasks
            GROUP BY status_id
        ''')

        # Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
        cur.execute('''
            SELECT users.fullname, tasks.title AS task
            FROM users
            INNER JOIN tasks ON tasks.user_id = users.id
            WHERE users.email LIKE ?
        ''',
            ('%@gmail.com',)
        )

        # Отримати список завдань, що не мають опису
        cur.execute('''
            SELECT * FROM tasks 
            WHERE description IS NULL
        ''')

        # Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
        cur.execute('''
            SELECT users.fullname, tasks.title AS task, status.name AS status
            FROM users
            LEFT JOIN tasks ON tasks.user_id = users.id
            INNER JOIN status ON status.id = tasks.status_id
            WHERE status.name = ?
            ''',
                ('in progress',)
        )

        conn.commit()


if __name__ == '__main__':
    call_requests()



