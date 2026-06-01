import os
import time
from contextlib import asynccontextmanager, contextmanager
from typing import Optional

import sqlalchemy
from fastapi import FastAPI, HTTPException, Request, Response
from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from pydantic import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    delete,
    insert,
    select,
    update,
)

metadata = MetaData()
tasks_table = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False),
    Column("done", Integer, default=0),
)

engine = sqlalchemy.create_engine(os.getenv("DATABASE_URL", "sqlite:///tasks.db"))

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)
http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
)
tasks_total = Gauge(
    "tasks_total",
    "Total number of tasks in the database",
)


def init_db():
    metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    endpoint = request.url.path
    http_requests_total.labels(
        method=request.method,
        endpoint=endpoint,
        status=str(response.status_code),
    ).inc()
    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=endpoint,
    ).observe(duration)
    return response


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@contextmanager
def get_db():
    with engine.connect() as conn:
        yield conn


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[int] = None


@app.get("/tasks")
def get_tasks():
    with get_db() as db:
        result = db.execute(select(tasks_table))
        rows = [dict(row._mapping) for row in result]
        tasks_total.set(len(rows))
        return rows


@app.post("/tasks", status_code=201)
def create_task(data: TaskCreate):
    with get_db() as db:
        result = db.execute(insert(tasks_table).values(title=data.title, done=0))
        db.commit()
    return {"id": result.inserted_primary_key[0], "title": data.title, "done": 0}


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate):
    with get_db() as db:
        task = db.execute(
            select(tasks_table).where(tasks_table.c.id == task_id)
        ).fetchone()
        if task is None:
            raise HTTPException(status_code=404, detail="not found")
        title = data.title if data.title is not None else task.title
        done = data.done if data.done is not None else task.done
        db.execute(
            update(tasks_table)
            .where(tasks_table.c.id == task_id)
            .values(title=title, done=done)
        )
        db.commit()
    return {"id": task_id, "title": title, "done": done}


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_db() as db:
        task = db.execute(
            select(tasks_table).where(tasks_table.c.id == task_id)
        ).fetchone()
        if task is None:
            raise HTTPException(status_code=404, detail="not found")
        db.execute(delete(tasks_table).where(tasks_table.c.id == task_id))
        db.commit()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
