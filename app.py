import sqlite3
from contextlib import contextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
DB_PATH = "tasks.db"


@contextmanager
def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()


def init_db():
    with get_db() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER DEFAULT 0
            )""")
        db.commit()


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[int] = None


@app.get("/tasks")
def get_tasks():
    with get_db() as db:
        tasks = db.execute("SELECT * FROM tasks").fetchall()
    return [dict(t) for t in tasks]


@app.post("/tasks", status_code=201)
def create_task(data: TaskCreate):
    with get_db() as db:
        cur = db.execute("INSERT INTO tasks (title) VALUES (?)", (data.title,))
        db.commit()
    return {"id": cur.lastrowid, "title": data.title, "done": 0}


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate):
    with get_db() as db:
        task = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if task is None:
            raise HTTPException(status_code=404, detail="not found")
        title = data.title if data.title is not None else task["title"]
        done = data.done if data.done is not None else task["done"]
        db.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?", (title, done, task_id)
        )
        db.commit()
    return {"id": task_id, "title": title, "done": done}


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_db() as db:
        task = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if task is None:
            raise HTTPException(status_code=404, detail="not found")
        db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        db.commit()


if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)
