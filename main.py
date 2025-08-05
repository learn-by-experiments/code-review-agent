from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.tasks import init_tasks_table, create_task, read_task, update_task, STATUS


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield init_tasks_table()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def root():
    return {"message": "code review agent is running"}


@app.get("/status/{task_id}")
async def get_status(task_id: int):
    return read_task(taskid=task_id)


@app.get("/results/{task_id}")
async def get_results(task_id: int):
    return read_task(taskid=task_id)


@app.put("/results/{task_id}")
async def update_results(task_id: int):
    result = {
        "task_id": task_id,
        "status": STATUS.COMPLETED,
        "results": {
            "files": [
                {
                    "name": "main.py",
                    "issues": [
                        {
                            "type": "style",
                            "line": 15,
                            "description": "Line too long",
                            "suggestion": "Break line into multiple lines",
                        },
                        {
                            "type": "bug",
                            "line": 23,
                            "description": "Potential null pointer",
                            "suggestion": "Add null check",
                        },
                    ],
                }
            ],
            "summary": {"total_files": 1, "total_issues": 2, "critical_issues": 1},
        },
    }
    return update_task(taskid=task_id, status=STATUS.COMPLETED, result=result)


@app.post("/analyze-pr")
async def analyze_pr():
    task_id = create_task()
    return {"task_id": task_id, "message": "code review is in progress"}
