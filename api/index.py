from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()
submissions = []

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Submission(BaseModel):
    user_id: str
    problem_id: str
    code: str

@app.get("/")
async def root():
    return {"message": "Coding Challenge API is running!", "status": "ok"}

@app.get("/problems")
def list_problems():
    problems = [
        "power-of-two", "three-sum", "binary-search-insert-position", 
        "elimination-game", "find-town-judge", "front-middle-back-queue",
        "insertion-sort-pairs", "longest-common-prefix", "max-path-sum-binary-tree",
        "merge-sort", "merge-two-sorted-lists", "regex-matching", 
        "stack-using-queues", "tiny-url-encoder"
    ]
    return {"problems": problems}

@app.post("/submit")
async def submit_code(submission: Submission):
    global submissions
    
    # Mock grading - gives 5/6 tests passed
    score = 5
    total = 6
    
    submission_entry = {
        "user_id": submission.user_id,
        "problem_id": submission.problem_id,
        "score": score,
        "replay_result": f"{score}/{total} tests passed",
        "timestamp": datetime.now().isoformat()
    }
    
    # Update leaderboard
    existing = next((entry for entry in submissions
                     if entry["user_id"] == submission.user_id and entry["problem_id"] == submission.problem_id), None)
    
    if existing:
        if submission_entry["score"] > existing["score"]:
            submissions = [s for s in submissions if s != existing]
            submissions.append(submission_entry)
    else:
        submissions.append(submission_entry)
    
    result = {
        "score": score,
        "total": total,
        "replay_result": "partially"
    }
    
    return {"grade": result, "leaderboard_entry": submission_entry}

@app.get("/leaderboard")
async def get_leaderboard():
    if not submissions:
        return {"leaderboard": []}

    sorted_subs = sorted(submissions, key=lambda x: (-x["score"], x["timestamp"]))
    
    leaderboard = []
    seen = set()
    
    for entry in sorted_subs:
        uid = entry["user_id"]
        if uid not in seen:
            leaderboard.append({
                "user_id": uid,
                "score": entry["score"],
                "replay_result": entry["replay_result"],
                "timestamp": entry["timestamp"]
            })
            seen.add(uid)
    
    return {"leaderboard": leaderboard}

@app.get("/problem/{problem_id}")
def get_problem_details(problem_id: str):
    return {
        "problem_id": problem_id,
        "public_tests": [
            {"input": "sample input", "expected_output": "sample output"}
        ],
        "hidden_tests_count": 5,
        "total_tests": 6
    }