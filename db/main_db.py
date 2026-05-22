import sqlite3
from config import path_db
from db import queries

def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.create_tasks_table)
    print('БД подключен')
    conn.commit()
    conn.close()
    
def add_task(task):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.insert_task,(task,))     #cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
        task_id = cursor.lastrowid
    return task_id

def update_task(task_id, new_task = None, completed = None ):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    if new_task is not None:
        cursor.execute(queries.update_task,(new_task,task_id))
    elif completed is not None:
        cursor.execute('UPDATE tasks SET completed  = ? WHERE id = ?',
        (completed,task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.delete_task,(task_id,))

def delete_completed():
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.delete_completed)
    
def get_task(filter_type = None):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    if filter_type == 'all':
        cursor.execute(queries.select_tasks)
    elif filter_type == 'completed':
        cursor.execute(queries.select_tasks_completed)
    elif filter_type == 'uncompleted':
        cursor.execute(queries.select_tasks_uncompleted)
    tasks = cursor.fetchall()
    conn.close()
    return tasks