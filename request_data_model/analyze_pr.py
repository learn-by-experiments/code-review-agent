from pydantic import BaseModel, HttpUrl


class PR(BaseModel):
    repo_url: HttpUrl
    pr_number: int
    github_token: str
