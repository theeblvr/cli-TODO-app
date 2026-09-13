import sqlite3
import datetime
from pathlib import Path
from typing import List

from models import Todo

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "todos.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


conn = get_connection()
c = conn.cursor()


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                task TEXT NOT NULL,
                category TEXT,
                date_added TEXT,
                date_completed TEXT,
                status INTEGER,
                position INTEGER
            )
            """
        )
        conn.commit()


init_db()


def insert_todo(todo: Todo):
    c.execute('SELECT COUNT(*) FROM todos')
    count = c.fetchone()[0]
    todo.position = count if count else 0

    with conn:
        c.execute(
            'INSERT INTO todos VALUES (:task, :category, :date_added, :date_completed, :status, :position)',
            {
                'task': todo.task,
                'category': todo.category,
                'date_added': todo.date_added,
                'date_completed': todo.date_completed,
                'status': todo.status,
                'position': todo.position,
            },
        )


def get_all_todos() -> List[Todo]:
    c.execute('SELECT * FROM todos')
    results = c.fetchall()
    todos = []
    for result in results:
        todos.append(Todo(*result))
    return todos


def delete_todo(position):
    c.execute('SELECT COUNT(*) FROM todos')
    count = c.fetchone()[0]

    with conn:
        c.execute('DELETE FROM todos WHERE position=:position', {'position': position})
        for pos in range(position + 1, count):
            change_position(pos, pos - 1, False)


def reset_todos():
    with conn:
        c.execute('DELETE FROM todos')


def change_position(old_position: int, new_position: int, commit=True):
    c.execute(
        'UPDATE todos SET position = :position_new WHERE position = :position_old',
        {'position_old': old_position, 'position_new': new_position},
    )
    if commit:
        conn.commit()


def update_todo(position: int, task: str, category: str):
    with conn:
        if task is not None and category is not None:
            c.execute(
                'UPDATE todos SET task = :task, category = :category WHERE position = :position',
                {'position': position, 'task': task, 'category': category},
            )
        elif task is not None:
            c.execute(
                'UPDATE todos SET task = :task WHERE position = :position',
                {'position': position, 'task': task},
            )
        elif category is not None:
            c.execute(
                'UPDATE todos SET category = :category WHERE position = :position',
                {'position': position, 'category': category},
            )


def complete_todo(position: int):
    with conn:
        c.execute(
            'UPDATE todos SET status = 2, date_completed = :date_completed WHERE position = :position',
            {'position': position, 'date_completed': datetime.datetime.now().isoformat()},
        )

