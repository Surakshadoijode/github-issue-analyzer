import requests

def fetch_issue_data(repo_url, issue_number):
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]

    issue_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    comments_url = issue_url + "/comments"

    issue_res = requests.get(issue_url)
    if issue_res.status_code != 200:
        raise Exception("Invalid repository or issue number")

    issue = issue_res.json()

    comments_res = requests.get(comments_url)
    comments = comments_res.json() if comments_res.status_code == 200 else []

    return {
        "title": issue.get("title", ""),
        "body": issue.get("body", ""),
        "comments": [c["body"] for c in comments]
    }
