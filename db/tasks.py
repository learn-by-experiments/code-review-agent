import psycopg2
from dotenv import load_dotenv
import json
import os

load_dotenv()


DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("USER_NAME"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
}


class STATUS:
    IN_PROGRESS = "in progress"
    FAILED = "failed"
    COMPLETED = "completed"


def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def init_tasks_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            taskid SERIAL PRIMARY KEY,
            status VARCHAR(50),
            result JSONB
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("********* Tasks Table Created ********")


def create_task(status=STATUS.IN_PROGRESS, result=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (status, result) VALUES (%s, %s) RETURNING taskid;",
        (status, json.dumps(result)),
    )
    taskid = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return taskid


def read_task(taskid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT taskid, status, result FROM tasks WHERE taskid = %s;", (taskid,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {"taskid": row[0], "status": row[1], "result": row[2]}
    return None


def update_task(taskid, status=None, result=None):
    conn = get_conn()
    cur = conn.cursor()
    row = None
    if status is not None and result is not None:
        cur.execute(
            "UPDATE tasks SET status = %s, result = %s WHERE taskid = %s RETURNING *;",
            (status, json.dumps(result), taskid),
        )
        row = cur.fetchone()
    elif status is not None:
        cur.execute(
            "UPDATE tasks SET status = %s WHERE taskid = %s RETURNING *;",
            (status, taskid),
        )
        row = cur.fetchone()
    elif result is not None:
        cur.execute(
            "UPDATE tasks SET result = %s WHERE taskid = %s RETURNING *;",
            (json.dumps(result), taskid),
        )
        row = cur.fetchone()
    if row:
        return {"taskid": row[0], "status": row[1], "result": row[2]}
    conn.commit()
    cur.close()
    conn.close()


def delete_task(taskid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE taskid = %s;", (taskid,))
    conn.commit()
    cur.close()
    conn.close()
