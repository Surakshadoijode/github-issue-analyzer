from fastapi import FastAPI, HTTPException
from schemas import IssueRequest, IssueAnalysis
from github_client import fetch_issue_data
from llm_analyzer import analyze_issue

app = FastAPI(title="GitHub Issue Analyzer")

@app.post("/analyze", response_model=IssueAnalysis)
def analyze(req: IssueRequest):
    try:
        issue_data = fetch_issue_data(req.repo_url, req.issue_number)
        analysis = analyze_issue(issue_data)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
