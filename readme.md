# GitHub Issue Analyzer 

A lightweight web application that analyzes GitHub issues using AI to help developers quickly understand, classify, and prioritize new issues.

The application accepts a **public GitHub repository URL** and an **issue number**, fetches issue details using the GitHub API, and generates a **structured summary** suitable for rapid triage and decision-making.

---

## Table of Contents

- Overview
- Features
- System Architecture
- Tech Stack
- Project Structure
- Setup Instructions
- Running the Application
- API Usage
- Example Output
- Fallback & Error Handling
- Design Decisions
- Conclusion

---

## Overview

At fast-moving development teams, quickly understanding incoming GitHub issues is critical.  
This project automates issue analysis by combining:

- GitHub API data retrieval  
- AI-driven reasoning  
- Structured output for consistency  

The result is a simple but robust tool that assists developers and maintainers in prioritizing issues efficiently.

---

## Features

- Accepts **any public GitHub repository**
- Fetches:
  - Issue title
  - Issue body
  - Issue comments
- Uses an **LLM** to generate structured analysis
- Produces output in a **fixed JSON schema**
- Simple and clean **Streamlit UI**
- **Graceful fallback mechanism** when the LLM is unavailable
- Handles edge cases such as:
  - Issues with no comments
  - Very long issue descriptions
  - External API failures

---

## System Architecture

Streamlit Frontend
↓
FastAPI Backend
↓
GitHub REST API + LLM
↓
Structured JSON Response

- **Frontend**: Collects input and displays results  
- **Backend**: Orchestrates data fetching and analysis  
- **AI Layer**: Performs reasoning and classification (with fallback support)

---

## Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: Streamlit
- **APIs**: GitHub REST API
- **LLM**: OpenAI (with rule-based fallback)
- **Utilities**: Requests, Pydantic, python-dotenv

---

## Project Structure

github-issue-analyzer/
├── backend/
│ ├── main.py     # FastAPI entry point
│ ├── github_client.py     # GitHub API integration
│ ├── llm_analyzer.py      # AI analysis + fallback logic
│ └── schemas.py      # Pydantic request/response models
├── frontend/
│ └── app.py     # Streamlit UI
├── .env.example      # Environment variable template
├── .gitignore
├── requirements.txt
└── README.md

yaml
Copy code

---

## Setup Instructions (Under 5 Minutes)

### 1. Clone the Repository
git clone <your-github-repository-link>
cd github-issue-analyzer

### 2. Create and Activate Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

### 3. Install Dependencies
pip install -r requirements.txt

### Environment Variables
Create a .env file in the project root (this file is not committed to GitHub):
OPENAI_API_KEY=your_openai_api_key_here
A reference file .env.example is included for clarity.

### Running the Application
Start the Backend (FastAPI)
cd backend
uvicorn main:app --reload
Backend URL: http://127.0.0.1:8000
API Docs: http://127.0.0.1:8000/docs

### Start the Frontend (Streamlit)
Open a new terminal, then:
cd frontend
streamlit run app.py

### Frontend runs at:
http://localhost:8501

### API Usage
### Endpoint
POST /analyze

### Request Body
{
  "repo_url": "https://github.com/facebook/react",
  "issue_number": 1
}

### Response Format
{
  "summary": "string",
  "type": "bug | feature_request | documentation | question | other",
  "priority_score": "1 to 5 with justification",
  "suggested_labels": ["string", "string"],
  "potential_impact": "string"
}

### Example Output
{
  "summary": "Run each test in its own iframe",
  "type": "feature_request",
  "priority_score": "2 – feature request with low immediate impact",
  "suggested_labels": ["needs-triage", "feature_request"],
  "potential_impact": "Minimal direct impact on existing users."
}

### Fallback & Error Handling
To ensure reliability, the system includes a graceful fallback mechanism:
--> If the LLM is unavailable due to:
    --> API quota limits
    --> Network failures
    --> Invalid AI responses
--> The system automatically switches to a rule-based classifier that:
    --> Determines issue type using heuristics
    --> Assigns a reasonable priority score
    --> Maintains the required JSON contract
This ensures the API never breaks the workflow, reflecting real-world production practices.

### Design Decisions
--> Separation of concerns between frontend, backend, and AI logic
--> Structured prompt engineering to enforce consistent JSON output
--> Defensive programming for external API dependencies
--> Readable and maintainable codebase
--> Modular AI layer for easy model replacement

### Conclusion
This project demonstrates an end-to-end AI-assisted workflow for GitHub issue triaging.
It combines API integration, AI reasoning, robust fallback handling, and a simple user interface to deliver a practical and production-aware solution.
