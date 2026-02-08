'''
You are assisting in the development of a Python desktop application focused on productivity tracking.

Project goals:
- Track real time spent on tasks
- Compare estimated time vs real time
- Persist data using SQLite (sqlite3, cursor-based)
- Clean, readable, maintainable code
- No unnecessary abstractions
- Follow separation of concerns

Constraints:
- Python 3.x
- sqlite3 module only (no ORM)
- Explicit SQL queries
- Clear function responsibilities
- Prefer simplicity over cleverness

When generating code:
- Explain complex logic briefly in comments
- Avoid overengineering
- Assume this code will be reviewed by a senior developer

'''

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "productivity.db")


def create_database():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            estimated_minutes INTEGER,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL,
            started_at TEXT,
            finished_at TEXT,
            real_minutes INTEGER
        )
    """)

    conexion.commit()
    conexion.close()


def create_task(title, estimated_minutes=None):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO tasks (title, estimated_minutes, status, created_at)
        VALUES (?, ?, 'pending', datetime('now'))
    """, (title, estimated_minutes))

    conexion.commit()
    conexion.close()
    
def get_tasks():
    conexion = sqlite3.connect( DB_PATH)
    cursor  = conexion.cursor()
    
    cursor.execute('''
            SELECT id, title, estimated_minutes, status, created_at
            FROM tasks
            ''')
    
    tareas = cursor.fetchall()
    
    conexion.commit()
    conexion.close()
    return tareas

def start_task(task_id):
    conexion = sqlite3.connect( DB_PATH)
    cursor = conexion.cursor()
    
    cursor.execute('''
                    UPDATE tasks
                    SET status = 'in_progress',
                        started_at = datetime('now')
                    WHERE id = ?
                   
                   ''',(task_id,))
    
    conexion.commit()
    conexion.close()
    
def finish_task(task_id):
    conexion = sqlite3.connect( DB_PATH)
    cursor = conexion.cursor()
    
    cursor.execute('''
           SELECT status FROM tasks WHERE id = ?    
    ''',(task_id,))
    
    result = cursor.fetchone()# Verificar que la tarea existe y está en progreso
    
    if not result:
        print(" La terea no existe.")
        conexion.close()
        return
    
    if result[0] != "in_progress":
        print("la tera no esta en progreso.")
        conexion.close()
        return
    
    cursor.execute("""
        UPDATE tasks
        SET status = 'done',
            finished_at = datetime('now'),
            real_minutes = (
                (strftime('%s', datetime('now')) - strftime('%s', started_at)) / 60
            )
        WHERE id = ?
    """, (task_id,))
    
    conexion.commit()
    conexion.close()
    print("Tarea finalizada correctamente.")

if __name__ == "__main__":
    create_database()
    create_task("Estudiar python", 60)
    
    start_task(1)
    input("Presiona Enter para finalizar la tarea...")
    
    finish_task(1)

    for task in get_tasks():
        print(task)
        

