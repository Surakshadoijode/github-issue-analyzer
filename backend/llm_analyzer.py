import os
import json
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def classify_fallback(issue):
    """
    Rule-based classification and priority scoring
    used when LLM is unavailable
    """
    title = issue.get("title", "").lower()
    body = issue.get("body", "").lower()
    text = title + " " + body

    # -------- TYPE CLASSIFICATION --------
    if "feature" in text or "request" in text or "enhancement" in text:
        issue_type = "feature_request"
    elif "doc" in text or "documentation" in text or "readme" in text:
        issue_type = "documentation"
    elif "?" in issue.get("title", ""):
        issue_type = "question"
    else:
        issue_type = "bug"

    # -------- PRIORITY SCORING --------
    if any(word in text for word in ["crash", "exception", "fatal", "error", "fails"]):
        priority = 5
        justification = "Critical issue causing crashes or failures"
    elif issue_type == "bug" and any(word in text for word in ["blocking", "unable", "breaks"]):
        priority = 4
        justification = "High impact bug blocking normal usage"
    elif issue_type == "bug":
        priority = 3
        justification = "Moderate impact bug affecting functionality"
    elif issue_type == "feature_request":
        priority = 2
        justification = "Feature request with low immediate impact"
    else:
        priority = 1
        justification = "Low priority informational issue"

    return {
        "summary": issue.get("title", "Issue summary unavailable"),
        "type": issue_type,
        "priority_score": f"{priority} – {justification}",
        "suggested_labels": ["needs-triage", issue_type],
        "potential_impact": (
            "Users may experience crashes or broken behavior."
            if issue_type == "bug"
            else "Minimal direct impact on users."
        )
    }


def analyze_issue(issue):
    """
    Analyze GitHub issue using LLM.
    Falls back to rule-based logic if LLM fails.
    """

    prompt = f"""
You are a senior software triage engineer.

Analyze the following GitHub issue and return ONLY valid JSON.
Do not include markdown or explanations.

{{
  "summary": "A one-sentence summary of the user's problem or request.",
  "type": "bug | feature_request | documentation | question | other",
  "priority_score": "A score from 1 (low) to 5 (critical), with a brief justification.",
  "suggested_labels": ["label1", "label2"],
  "potential_impact": "A brief sentence on the potential impact on users."
}}

Issue Title:
{issue.get("title", "")}

Issue Body:
{issue.get("body", "")[:4000]}

Comments:
{issue.get("comments", [])[:5]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return json.loads(response.choices[0].message.content)

    except (OpenAIError, json.JSONDecodeError):
        return classify_fallback(issue)
