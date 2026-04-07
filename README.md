# Job Application Tracker API

A RESTful API built with FastAPI to track and manage job applications.

## Features
- Add job applications
- View all applications
- Filter by status
- View application statistics

## Tech Stack
- Python (FastAPI)
- SQLAlchemy
- SQLite

## How to Run Locally
1. Clone the repo: `git clone https://github.com/darthouse101/job-tracker-api.git`
2. Install dependencies: `pip install fastapi uvicorn sqlalchemy`
3. Start the server: `python -m uvicorn main:app --reload`
4. Open browser: `http://127.0.0.1:8000/docs` to interact with the API