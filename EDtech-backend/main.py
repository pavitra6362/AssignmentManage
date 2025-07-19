from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI()

# Allow frontend calls (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulated database (in-memory)
users = []
assignments = []
submissions = []

# Models
class User(BaseModel):
    id: str
    name: str
    email: str
    password: str
    role: str  # student or teacher

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

class UserLogin(BaseModel):
    email: str
    password: str

class Assignment(BaseModel):
    id: str
    title: str
    description: str
    due_date: str
    teacher_id: str

class AssignmentCreate(BaseModel):
    title: str
    description: str
    due_date: str
    teacher_id: str

class Submission(BaseModel):
    id: str
    assignment_id: str
    student_id: str
    content: str
    submitted_at: str

class SubmissionCreate(BaseModel):
    assignment_id: str
    student_id: str
    content: str
    submitted_at: str

# Routes
@app.post("/signup")
def signup(user: UserCreate):
    for u in users:
        if u.email == user.email:
            raise HTTPException(status_code=400, detail="Email already exists")
    new_user = User(id=str(uuid4()), **user.dict())
    users.append(new_user)
    return {"message": "User created"}

@app.post("/login")
def login(data: UserLogin):
    for u in users:
        if u.email == data.email and u.password == data.password:
            return u
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/assignments")
def create_assignment(assignment: AssignmentCreate):
    new_assign = Assignment(id=str(uuid4()), **assignment.dict())
    assignments.append(new_assign)
    return {"message": "Assignment created"}

@app.get("/assignments", response_model=List[Assignment])
def get_assignments():
    return assignments

@app.post("/submit")
def submit_assignment(sub: SubmissionCreate):
    new_sub = Submission(id=str(uuid4()), **sub.dict())
    submissions.append(new_sub)
    return {"message": "Submission successful"}

@app.get("/submissions/{assignment_id}")
def get_submissions(assignment_id: str):
    return [s for s in submissions if s.assignment_id == assignment_id]
