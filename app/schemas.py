from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal, List
from datetime import date

# ---------- Auth ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)

class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    role: str

# ---------- Tasks ----------
TaskStatus = Literal["pending", "in_progress", "done"]

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default="", max_length=5000)
    status: TaskStatus = "pending"
    priority: int = Field(default=3, ge=1, le=5)
    due_date: Optional[date] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: int

class PaginatedTasks(BaseModel):
    items: List[TaskOut]
    total: int
    skip: int
    limit: int
