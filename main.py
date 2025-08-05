from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import requests
from agents.code_review_agent import code_review_agent
from request_data_model.analyze_pr import PR
from db.tasks import init_tasks_table, create_task, read_task


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


# @app.put("/results/{task_id}")
# async def update_results(task_id: int):
#     result = {
#         "task_id": task_id,
#         "status": STATUS.COMPLETED,
#         "results": {
#             "files": [
#                 {
#                     "name": "main.py",
#                     "issues": [
#                         {
#                             "type": "style",
#                             "line": 15,
#                             "description": "Line too long",
#                             "suggestion": "Break line into multiple lines",
#                         },
#                         {
#                             "type": "bug",
#                             "line": 23,
#                             "description": "Potential null pointer",
#                             "suggestion": "Add null check",
#                         },
#                     ],
#                 }
#             ],
#             "summary": {"total_files": 1, "total_issues": 2, "critical_issues": 1},
#         },
#     }
#     return update_task(taskid=task_id, status=STATUS.COMPLETED, result=result)


@app.post("/analyze-pr")
async def analyze_pr(pr: PR):
    task_id = create_task()
    if pr.repo_url.host != "github.com":
        raise HTTPException(
            status_code=400,
            detail="Invalid Repo URL. Host must be github.com. Correct URL format : https://github.com/user/repo",
        )
    path_parameters = pr.repo_url.path.split("/")
    if len(path_parameters) != 3:
        raise HTTPException(
            status_code=400,
            detail="Invalid Repo URL. Onwer and repo should not be null. Correct URL format : https://github.com/user/repo",
        )
    first, owner, repo = path_parameters
    personal_access_token = pr.github_token
    pull_request_no = pr.pr_number
    print(personal_access_token)
    res = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_request_no}",
        headers={
            "Authorization": f"Bearer {personal_access_token}",
            "Accept": "application/vnd.github.diff",
        },
    )
    print(code_review_agent.invoke({"messages": res.content.decode()}))
    return {"task_id": task_id, "message": "code review is in progress"}
