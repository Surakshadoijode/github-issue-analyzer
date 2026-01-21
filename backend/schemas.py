from pydantic import BaseModel
from typing import List

class IssueRequest(BaseModel):
    repo_url: str
    issue_number: int

class IssueAnalysis(BaseModel):
    summary: str
    type: str
    priority_score: str
    suggested_labels: List[str]
    potential_impact: str
